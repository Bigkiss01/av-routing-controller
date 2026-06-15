document.addEventListener('DOMContentLoaded', () => {
    // --- Navigation ---
    const navBtns = document.querySelectorAll('.nav-btn');
    const views = document.querySelectorAll('.view-section');

    navBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            navBtns.forEach(b => b.classList.remove('active'));
            views.forEach(v => v.classList.remove('active'));
            
            btn.classList.add('active');
            document.getElementById(btn.dataset.target).classList.add('active');
        });
    });

    // --- State ---
    let devices = [];
    let selectedEncoderId = null;

    // --- Toast Notification ---
    function showToast(message, isError = false) {
        const toast = document.getElementById('toast');
        toast.textContent = message;
        if(isError) toast.classList.add('error');
        else toast.classList.remove('error');
        
        toast.classList.remove('hidden');
        setTimeout(() => toast.classList.add('hidden'), 3000);
    }

    // --- API Calls ---
    async function fetchDevices() {
        try {
            const res = await fetch('/api/devices');
            devices = await res.json();
            renderDevicesTable();
            renderMatrixGrid();
        } catch (e) {
            showToast('Failed to load devices from Control Server', true);
        }
    }

    async function routeVideo(encoderId, decoderIds) {
        try {
            const res = await fetch('/api/route', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ encoder_id: encoderId, decoder_ids: decoderIds })
            });
            const data = await res.json();
            if(res.ok) {
                showToast(data.message);
                // Refresh list to potentially get updated status
                setTimeout(fetchDevices, 1000);
            } else {
                showToast(data.message, true);
            }
        } catch (e) {
            showToast('Failed to route video', true);
        }
    }

    // --- UI Renderers ---
    function renderDevicesTable() {
        const tbody = document.querySelector('#devices-table tbody');
        tbody.innerHTML = '';
        if (!devices || devices.length === 0) {
            tbody.innerHTML = '<tr><td colspan="4" style="text-align:center; color: var(--text-muted)">No devices synced. Is VAVE Server (192.168.2.10) online?</td></tr>';
            return;
        }
        devices.forEach(dev => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td><strong>${dev.name}</strong> <span class="text-muted">(ID: ${dev.id})</span></td>
                <td>${dev.ip}</td>
                <td><span style="color: ${dev.role === 'encoder' ? 'var(--accent)' : 'var(--primary)'}">${dev.role.toUpperCase()}</span></td>
                <td><span class="text-muted" style="font-size:0.8rem">Auto Synced</span></td>
            `;
            tbody.appendChild(tr);
        });
    }

    function renderMatrixGrid() {
        const encodersList = document.getElementById('encoders-list');
        const decodersList = document.getElementById('decoders-list');
        const btnApply = document.getElementById('btn-apply-route');
        
        const encoders = devices.filter(d => d.role === 'encoder');
        const decoders = devices.filter(d => d.role === 'decoder');

        // Render Encoders (Left Panel)
        encodersList.innerHTML = '';
        if(encoders.length === 0) {
            encodersList.innerHTML = '<p class="text-muted">No encoders synced.</p>';
        } else {
            encoders.forEach(enc => {
                const card = document.createElement('div');
                card.className = `device-card encoder-card ${selectedEncoderId === enc.id ? 'selected' : ''}`;
                card.draggable = true;
                card.dataset.id = enc.id;
                
                card.innerHTML = `
                    <h4>${enc.name}</h4>
                    <p style="margin-bottom:0">IP: ${enc.ip}</p>
                    <div class="status-dot"></div>
                `;

                // Click to select
                card.addEventListener('click', () => {
                    selectedEncoderId = enc.id;
                    btnApply.disabled = false;
                    renderMatrixGrid();
                });

                // Drag start
                card.addEventListener('dragstart', (e) => {
                    e.dataTransfer.setData('text/plain', enc.id);
                    e.dataTransfer.effectAllowed = 'copy';
                });

                encodersList.appendChild(card);
            });
        }

        // Render Decoders (Right Panel)
        decodersList.innerHTML = '';
        if(decoders.length === 0) {
            decodersList.innerHTML = '<p class="text-muted">No decoders synced.</p>';
            btnApply.disabled = true;
        } else {
            decoders.forEach(dec => {
                const card = document.createElement('div');
                card.className = 'device-card decoder-card';
                card.dataset.id = dec.id;

                card.innerHTML = `
                    <div class="card-header-flex">
                        <div>
                            <h4>${dec.name}</h4>
                            <p style="margin-bottom:0">IP: ${dec.ip}</p>
                        </div>
                        <input type="checkbox" class="custom-checkbox decoder-checkbox" value="${dec.id}">
                    </div>
                    <div class="active-source-badge">
                        <span class="badge-text">Auto Synced Node</span>
                        <span class="badge-value"></span>
                    </div>
                `;

                // Click on card checks the box
                card.addEventListener('click', (e) => {
                    if(e.target.type !== 'checkbox') {
                        const cb = card.querySelector('.decoder-checkbox');
                        cb.checked = !cb.checked;
                    }
                });

                // Drop target logic
                card.addEventListener('dragover', (e) => {
                    e.preventDefault(); // allow drop
                    card.classList.add('active-drop');
                    e.dataTransfer.dropEffect = 'copy';
                });

                card.addEventListener('dragleave', () => {
                    card.classList.remove('active-drop');
                });

                card.addEventListener('drop', (e) => {
                    e.preventDefault();
                    card.classList.remove('active-drop');
                    const draggedEncoderId = e.dataTransfer.getData('text/plain');
                    if(draggedEncoderId) {
                        routeVideo(draggedEncoderId, [dec.id]);
                    }
                });

                decodersList.appendChild(card);
            });
        }
        
        if(!selectedEncoderId) btnApply.disabled = true;
    }

    // --- Panel Buttons ---
    document.getElementById('btn-select-all').addEventListener('click', () => {
        document.querySelectorAll('.decoder-checkbox').forEach(cb => cb.checked = true);
    });

    document.getElementById('btn-clear-all').addEventListener('click', () => {
        document.querySelectorAll('.decoder-checkbox').forEach(cb => cb.checked = false);
    });

    document.getElementById('btn-apply-route').addEventListener('click', () => {
        if(!selectedEncoderId) return;
        const checkedBoxes = document.querySelectorAll('.decoder-checkbox:checked');
        const decoderIds = Array.from(checkedBoxes).map(cb => cb.value);
        
        if(decoderIds.length === 0) {
            showToast('Please select at least one display target', true);
            return;
        }
        routeVideo(selectedEncoderId, decoderIds);
    });

    // --- Global Drop Area ---
    const outputsPanel = document.querySelector('.outputs-panel');
    outputsPanel.addEventListener('dragover', (e) => {
        e.preventDefault();
        outputsPanel.classList.add('drag-over');
    });
    outputsPanel.addEventListener('dragleave', (e) => {
        if(!outputsPanel.contains(e.relatedTarget)) {
            outputsPanel.classList.remove('drag-over');
        }
    });
    outputsPanel.addEventListener('drop', (e) => {
        e.preventDefault();
        outputsPanel.classList.remove('drag-over');
        const draggedEncoderId = e.dataTransfer.getData('text/plain');
        if(draggedEncoderId) {
            const checkedBoxes = document.querySelectorAll('.decoder-checkbox:checked');
            const decoderIds = Array.from(checkedBoxes).map(cb => cb.value);
            if(decoderIds.length > 0) {
                routeVideo(draggedEncoderId, decoderIds);
            } else {
                showToast('Drop on a specific card, or select checkboxes first.', true);
            }
        }
    });

    // Disable device form since we auto-sync now
    const formBtn = document.querySelector('#device-form button[type="submit"]');
    if (formBtn) {
        formBtn.disabled = true;
        formBtn.textContent = "Disabled (Auto Synced from Server)";
    }

    // --- Init ---
    fetchDevices();
});
