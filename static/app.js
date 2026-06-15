document.addEventListener('DOMContentLoaded', () => {
    // --- Translations Dictionary ---
    const translations = {
        en: {
            "sidebar.subtitle": "AV over IP Control",
            "sidebar.developed_by": "Developed by",
            "nav.matrix": "Matrix Router",
            "nav.templates": "Routing Templates",
            "nav.setup": "Device Setup",
            "nav.scanner": "Network Scanner",
            "matrix.title": "AV Matrix Switcher",
            "matrix.subtitle": "Route Encoders (Inputs) to Decoders (Outputs)",
            "matrix.select_input": "1. Select Input Source",
            "matrix.select_output": "2. Choose Display Targets",
            "matrix.select_all": "Select All",
            "matrix.clear": "Clear",
            "matrix.instructions": "Select displays to switch or drop an input card here:",
            "matrix.apply_switch": "Apply Route Switch",
            "matrix.quick_save": "💾 Quick Save",
            "templates.title": "Routing Templates",
            "templates.subtitle": "Switch inputs and outputs simultaneously via presets",
            "templates.enter_admin": "🔒 Enter Admin Mode",
            "templates.exit_admin": "🔓 Exit Admin Mode",
            "templates.new_preset": "➕ New Template",
            "templates.empty_state": "No templates configured yet. Click 'New Template' in Admin Mode.",
            "setup.title": "Device Setup",
            "setup.subtitle": "Configure IP addresses, names, and roles.",
            "setup.add_device_title": "Add/Update Device",
            "setup.ip_label": "IP Address",
            "setup.name_label": "Device Name",
            "setup.role_label": "Role",
            "setup.role_encoder": "Encoder (Input)",
            "setup.role_decoder": "Decoder (Output)",
            "setup.save_device_btn": "Save Device",
            "setup.configured_title": "Configured Devices",
            "setup.col_name": "Name",
            "setup.col_ip": "IP Address",
            "setup.col_role": "Role",
            "setup.col_action": "Action",
            "admin_settings.title": "General Admin Settings",
            "admin_settings.default_lang": "Default System Language",
            "admin_settings.save_btn": "Save Settings",
            "admin_settings.change_pin_title": "Change Admin PIN",
            "admin_settings.old_pin": "Old PIN",
            "admin_settings.new_pin": "New PIN",
            "admin_settings.change_pin_btn": "Change PIN",
            "scanner.title": "Network Scanner",
            "scanner.subtitle": "Discover VAVE devices on the local network.",
            "scanner.start_btn": "Start Scan",
            "scanner.discovered_title": "Discovered Devices",
            "scanner.empty_state": "No scan performed yet.",
            "modal_template.create_title": "Create Template",
            "modal_template.edit_title": "Edit Template",
            "modal_template.name_label": "Template Name",
            "modal_template.desc_label": "Description (Optional)",
            "modal_template.color_label": "Color Theme",
            "modal_template.icon_label": "Icon (Emoji)",
            "modal_template.routing_title": "Routing Configuration",
            "modal_template.add_row": "➕ Add Route",
            "common.cancel": "Cancel",
            "common.save": "Save Template",
            "modal_pin.title": "Enter Admin PIN",
            "modal_pin.subtitle": "Please enter the 4-digit PIN code to unlock edit mode",
            "modal_pin.error": "Invalid PIN code",
            "modal_pin.verify": "Verify",
            "modal_confirm.title": "Apply Template Preset",
            "modal_confirm.subtitle": "Are you sure you want to apply this preset?",
            "modal_confirm.apply": "Apply",
            // Dynamic text mappings
            "active_source": "Active Source",
            "confirm_del": "Are you sure you want to delete template \"{name}\"?",
            "err_no_routes": "Please add at least 1 routing configuration.",
            "err_no_devices": "No active display devices found to save.",
            "toast_pin_success": "Admin Mode enabled",
            "toast_pin_exit": "Admin Mode disabled",
            "toast_pin_autolock": "Admin Mode locked due to inactivity",
            "toast_pin_update": "Admin PIN updated successfully",
            "toast_config_update": "System configuration updated successfully",
            "toast_quick_save_empty": "No active routes to save right now."
        },
        th: {
            "sidebar.subtitle": "ระบบควบคุม AV over IP",
            "sidebar.developed_by": "พัฒนาโดย",
            "nav.matrix": "หน้าควบคุมหลัก",
            "nav.templates": "เทมเพลตสลับสัญญาณ",
            "nav.setup": "ตั้งค่าอุปกรณ์",
            "nav.scanner": "ค้นหาอุปกรณ์",
            "matrix.title": "เครื่องสลับสัญญาณภาพและเสียง",
            "matrix.subtitle": "สลับอินพุต (ตัวส่ง) ไปยังเอาต์พุต (จอแสดงผล)",
            "matrix.select_input": "1. เลือกแหล่งสัญญาณอินพุต",
            "matrix.select_output": "2. เลือกจอแสดงผลปลายทาง",
            "matrix.select_all": "เลือกทั้งหมด",
            "matrix.clear": "ล้างการเลือก",
            "matrix.instructions": "เลือกจอแสดงผลที่ต้องการสลับ หรือลากการ์ดอินพุตมาวางที่นี่:",
            "matrix.apply_switch": "ยืนยันสลับสัญญาณ",
            "matrix.quick_save": "💾 บันทึกด่วน",
            "templates.title": "เทมเพลตและพรีเซ็ต",
            "templates.subtitle": "สลับอินพุตและเอาต์พุตพร้อมกันผ่านปุ่มลัด (Presets)",
            "templates.enter_admin": "🔒 เข้าสู่โหมดผู้ดูแลระบบ",
            "templates.exit_admin": "🔓 ออกจากโหมดผู้ดูแลระบบ",
            "templates.new_preset": "➕ สร้างเทมเพลตใหม่",
            "templates.empty_state": "ยังไม่มีเทมเพลตที่ตั้งค่าไว้ คลิก 'สร้างเทมเพลตใหม่' ในโหมดผู้ดูแลระบบ",
            "setup.title": "ตั้งค่าอุปกรณ์",
            "setup.subtitle": "กำหนดค่าที่อยู่ IP, ชื่ออุปกรณ์ และหน้าที่การทำงาน",
            "setup.add_device_title": "เพิ่ม/อัปเดตอุปกรณ์",
            "setup.ip_label": "ที่อยู่ IP",
            "setup.name_label": "ชื่ออุปกรณ์",
            "setup.role_label": "บทบาทหน้าที่",
            "setup.role_encoder": "ตัวส่งสัญญาณ (Encoder)",
            "setup.role_decoder": "ตัวรับสัญญาณ (Decoder)",
            "setup.save_device_btn": "บันทึกข้อมูลอุปกรณ์",
            "setup.configured_title": "อุปกรณ์ที่ตั้งค่าไว้",
            "setup.col_name": "ชื่ออุปกรณ์",
            "setup.col_ip": "ที่อยู่ IP",
            "setup.col_role": "บทบาท",
            "setup.col_action": "การจัดการ",
            "admin_settings.title": "ตั้งค่าระบบทั่วไป (Admin)",
            "admin_settings.default_lang": "ภาษาเริ่มต้นของระบบ",
            "admin_settings.save_btn": "บันทึกการตั้งค่า",
            "admin_settings.change_pin_title": "เปลี่ยนรหัส PIN ผู้ดูแลระบบ",
            "admin_settings.old_pin": "รหัส PIN เดิม",
            "admin_settings.new_pin": "รหัส PIN ใหม่",
            "admin_settings.change_pin_btn": "เปลี่ยนรหัส PIN",
            "scanner.title": "ค้นหาอุปกรณ์ในระบบ",
            "scanner.subtitle": "สแกนค้นหาอุปกรณ์ VAVE ในวงเครือข่ายท้องถิ่น",
            "scanner.start_btn": "เริ่มสแกน",
            "scanner.discovered_title": "อุปกรณ์ที่ค้นพบ",
            "scanner.empty_state": "ยังไม่ได้ทำการสแกนค้นหา",
            "modal_template.create_title": "สร้างเทมเพลตสลับสัญญาณ",
            "modal_template.edit_title": "แก้ไขเทมเพลตสลับสัญญาณ",
            "modal_template.name_label": "ชื่อเทมเพลต",
            "modal_template.desc_label": "คำอธิบาย (ไม่บังคับ)",
            "modal_template.color_label": "สีธีมปุ่ม",
            "modal_template.icon_label": "ไอคอน (Emoji)",
            "modal_template.routing_title": "การกำหนดแผนผังสลับสัญญาณ",
            "modal_template.add_row": "➕ เพิ่มการสลับสัญญาณ",
            "common.cancel": "ยกเลิก",
            "common.save": "บันทึกเทมเพลต",
            "modal_pin.title": "กรอกรหัส PIN ผู้ดูแลระบบ",
            "modal_pin.subtitle": "โปรดป้อนรหัส PIN 4 หลักเพื่อปลดล็อคโหมดแก้ไข",
            "modal_pin.error": "รหัส PIN ไม่ถูกต้อง",
            "modal_pin.verify": "ยืนยัน",
            "modal_confirm.title": "ใช้งานเทมเพลตสลับสัญญาณ",
            "modal_confirm.subtitle": "คุณต้องการใช้งานพรีเซ็ตนี้ใช่หรือไม่?",
            "modal_confirm.apply": "ใช้งาน",
            // Dynamic text mappings
            "active_source": "สัญญาณที่แสดงอยู่",
            "confirm_del": "ต้องการลบเทมเพลต \"{name}\" ใช่หรือไม่?",
            "err_no_routes": "โปรดตั้งค่าการจัดเส้นทางอย่างน้อย 1 รายการ",
            "err_no_devices": "ไม่พบข้อมูลหน้าจอที่ใช้งานอยู่ ไม่สามารถบันทึกได้",
            "toast_pin_success": "เข้าสู่โหมด Admin สำเร็จ",
            "toast_pin_exit": "ออกจากโหมด Admin แล้ว",
            "toast_pin_autolock": "ระบบทำการ Auto-lock โหมด Admin เนื่องจากไม่มีการใช้งาน",
            "toast_pin_update": "เปลี่ยนรหัส Admin PIN สำเร็จ",
            "toast_config_update": "บันทึกค่าภาษาเริ่มต้นของระบบสำเร็จ",
            "toast_quick_save_empty": "ไม่มีการเชื่อมโยงสัญญาณใดๆ ในขณะนี้ ไม่สามารถบันทึกได้"
        }
    };

    // --- State ---
    let devices = [];
    let templates = [];
    let selectedEncoderId = null;
    let activeTemplateId = null;
    let isAdminMode = false;
    let adminPin = "";
    let adminTimeout = null;
    let currentLanguage = 'th'; // default language state

    // --- Multi-Language Functions ---
    function applyLanguage(lang) {
        currentLanguage = lang;
        
        // Update active class on switcher
        document.querySelectorAll('.lang-btn').forEach(btn => {
            if (btn.dataset.lang === lang) {
                btn.classList.add('active');
            } else {
                btn.classList.remove('active');
            }
        });

        // Translate text elements with data-i18n attributes
        document.querySelectorAll('[data-i18n]').forEach(el => {
            const key = el.dataset.i18n;
            if (translations[lang][key]) {
                // If it contains HTML elements inside (like <strong> in разработан) handle selectively
                if (key === 'sidebar.developed_by') {
                    el.innerHTML = `${translations[lang][key]}`;
                } else {
                    el.textContent = translations[lang][key];
                }
            }
        });

        // Translate input placeholders
        const placeholders = {
            'scan-subnet': lang === 'en' ? 'Subnet (e.g., 192.168.1.0/24)' : 'ช่วงเครือข่าย เช่น 192.168.1.0/24',
            'dev-ip': lang === 'en' ? 'e.g. 192.168.1.10' : 'เช่น 192.168.1.10',
            'dev-name': lang === 'en' ? 'e.g. Input PC 1' : 'เช่น คอมพิวเตอร์นำเสนอ 1',
            'template-name': lang === 'en' ? 'e.g. Presentation Mode' : 'เช่น โหมดนำเสนอความรู้',
            'template-desc': lang === 'en' ? 'e.g. HDMI1 to TV1 & TV2' : 'เช่น HDMI1 ออกจอ TV1 และ TV2',
            'admin-pin-input': '••••',
            'pin-old': '••••',
            'pin-new': '••••'
        };

        for (const [id, val] of Object.entries(placeholders)) {
            const input = document.getElementById(id);
            if (input) input.placeholder = val;
        }

        // Re-render components that construct raw text dynamically
        renderMatrixGrid();
        renderTemplateGrid();
    }

    function changeLanguage(lang) {
        localStorage.setItem('metrix_language', lang);
        applyLanguage(lang);
    }

    // Connect language switch trigger buttons
    document.querySelectorAll('.lang-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            changeLanguage(btn.dataset.lang);
        });
    });

    // --- Navigation Logic ---
    const navBtns = document.querySelectorAll('.nav-btn');
    const viewSections = document.querySelectorAll('.view-section');

    function navigateTo(targetId) {
        // Hide all sections
        viewSections.forEach(section => {
            section.classList.remove('active');
        });
        // Remove active from all nav buttons
        navBtns.forEach(btn => {
            btn.classList.remove('active');
        });
        // Show target section
        const targetSection = document.getElementById(targetId);
        if (targetSection) {
            targetSection.classList.add('active');
        }
        // Set active nav button
        const targetBtn = document.querySelector(`.nav-btn[data-target="${targetId}"]`);
        if (targetBtn) {
            targetBtn.classList.add('active');
        }
    }

    navBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const target = btn.dataset.target;
            if (target) navigateTo(target);
        });
    });

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
            await fetchTemplates();
        } catch (e) {
            showToast(currentLanguage === 'en' ? 'Failed to load devices' : 'ไม่สามารถโหลดข้อมูลอุปกรณ์ได้', true);
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
                showToast(currentLanguage === 'en' ? 'Video routed successfully' : 'สลับสัญญาณสำเร็จ');
                activeTemplateId = null;
                renderTemplateGrid();
                setTimeout(fetchDevices, 1000);
            } else {
                showToast(data.message, true);
            }
        } catch (e) {
            showToast(currentLanguage === 'en' ? 'Failed to route video' : 'การสลับสัญญาณล้มเหลว', true);
        }
    }

    // --- Helper function to get source name ---
    function getSourceName(sourceId) {
        if (!sourceId || sourceId === '' || sourceId === '0') return currentLanguage === 'en' ? 'None' : 'ไม่มี';
        const enc = devices.find(d => d.role === 'encoder' && d.id === sourceId);
        return enc ? enc.name : `${currentLanguage === 'en' ? 'Input' : 'อินพุต'} ${sourceId}`;
    }

    // --- UI Renderers ---
    function renderDevicesTable() {
        const tbody = document.querySelector('#devices-table tbody');
        tbody.innerHTML = '';
        if (!devices || devices.length === 0) {
            const emptyText = currentLanguage === 'en' 
                ? 'No devices synced. Is VAVE Server online?' 
                : 'ไม่พบอุปกรณ์ที่เชื่อมต่อ ตรวจสอบว่าเครื่องเซิร์ฟเวอร์เปิดอยู่หรือไม่';
            tbody.innerHTML = `<tr><td colspan="4" style="text-align:center; color: var(--text-muted)">${emptyText}</td></tr>`;
            return;
        }
        devices.forEach(dev => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td><strong>${dev.name}</strong> <span class="text-muted">(ID: ${dev.id})</span></td>
                <td>${dev.ip}</td>
                <td><span style="color: ${dev.role === 'encoder' ? 'var(--accent)' : 'var(--primary)'}">${dev.role.toUpperCase()}</span></td>
                <td><span class="text-muted" style="font-size:0.8rem">${currentLanguage === 'en' ? 'Auto Synced' : 'เชื่อมต่ออัตโนมัติ'}</span></td>
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
            encodersList.innerHTML = `<p class="text-muted">${currentLanguage === 'en' ? 'No encoders synced.' : 'ไม่พบแหล่งสัญญาณอินพุต'}</p>`;
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
            decodersList.innerHTML = `<p class="text-muted">${currentLanguage === 'en' ? 'No decoders synced.' : 'ไม่พบจอแสดงผลเอาต์พุต'}</p>`;
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
                        <span class="badge-text">${translations[currentLanguage]["active_source"]}</span>
                        <span class="badge-value">${getSourceName(dec.source_id)}</span>
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
                    e.preventDefault();
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
            showToast(currentLanguage === 'en' ? 'Please select at least one display target' : 'โปรดเลือกจอแสดงผลปลายทางอย่างน้อย 1 จอ', true);
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
                showToast(currentLanguage === 'en' ? 'Drop on a display card, or select checkboxes first.' : 'โปรดลากวางบนการ์ดจอแสดงผล หรือเลือกกล่องเครื่องหมายก่อน', true);
            }
        }
    });

    // Disable device form since we auto-sync now
    const formBtn = document.querySelector('#device-form button[type="submit"]');
    if (formBtn) {
        formBtn.disabled = true;
        formBtn.textContent = currentLanguage === 'en' ? "Disabled (Auto Synced)" : "ปิดใช้งาน (ซิงค์อัตโนมัติจากเซิร์ฟเวอร์)";
    }

    // ==========================================
    // --- TEMPLATE & ADMIN LOGIC ---
    // ==========================================

    // --- Fetch Templates ---
    async function fetchTemplates() {
        try {
            const res = await fetch('/api/templates');
            templates = await res.json();
            renderTemplateGrid();
        } catch (e) {
            showToast(currentLanguage === 'en' ? 'Failed to load templates' : 'โหลดเทมเพลตไม่สำเร็จ', true);
        }
    }

    // --- Save/Update Template ---
    async function saveTemplate(templateData) {
        const id = templateData.id;
        const url = id ? `/api/templates/${id}` : '/api/templates';
        const method = id ? 'PUT' : 'POST';
        
        try {
            const res = await fetch(url, {
                method: method,
                headers: {
                    'Content-Type': 'application/json',
                    'X-Admin-PIN': adminPin
                },
                body: JSON.stringify(templateData)
            });
            const data = await res.json();
            if (res.ok) {
                showToast(currentLanguage === 'en' ? 'Preset saved successfully' : 'บันทึกพรีเซ็ตสำเร็จ');
                closeTemplateModal();
                await fetchTemplates();
            } else {
                showToast(data.error || 'Failed to save template', true);
            }
        } catch (e) {
            showToast('Network error saving template', true);
        }
    }

    // --- Delete Template ---
    async function deleteTemplate(id) {
        try {
            const res = await fetch(`/api/templates/${id}`, {
                method: 'DELETE',
                headers: {
                    'X-Admin-PIN': adminPin
                }
            });
            const data = await res.json();
            if (res.ok) {
                showToast(currentLanguage === 'en' ? 'Template deleted successfully' : 'ลบเทมเพลตเรียบร้อย');
                await fetchTemplates();
            } else {
                showToast(data.error || 'Failed to delete template', true);
            }
        } catch (e) {
            showToast('Network error deleting template', true);
        }
    }

    // --- Apply Template ---
    async function applyTemplate(id) {
        try {
            const res = await fetch(`/api/templates/${id}/apply`, {
                method: 'POST'
            });
            const data = await res.json();
            if (res.ok) {
                const tpl = templates.find(t => t.id === id);
                const name = tpl ? tpl.name : '';
                showToast(currentLanguage === 'en' ? `Preset "${name}" applied` : `ใช้งานพรีเซ็ต "${name}" สำเร็จ`);
                activeTemplateId = id;
                renderTemplateGrid();
                setTimeout(fetchDevices, 1000);
            } else {
                showToast(data.message || 'Failed to apply template', true);
            }
        } catch (e) {
            showToast('Network error applying template', true);
        }
    }

    // --- Admin Mode UI Management ---
    function updateAdminUI() {
        const btnLock = document.getElementById('btn-admin-lock');
        const btnNew = document.getElementById('btn-new-template');
        const btnQuickSave = document.getElementById('btn-quick-save');
        const adminPanel = document.getElementById('admin-settings-panel');
        
        if (isAdminMode) {
            btnLock.textContent = translations[currentLanguage]["templates.exit_admin"];
            btnLock.classList.remove('outline');
            btnLock.classList.add('danger');
            btnNew.classList.remove('hidden');
            if (btnQuickSave) btnQuickSave.style.display = 'block';
            if (adminPanel) adminPanel.classList.remove('hidden');
        } else {
            btnLock.textContent = translations[currentLanguage]["templates.enter_admin"];
            btnLock.classList.add('outline');
            btnLock.classList.remove('danger');
            btnNew.classList.add('hidden');
            if (btnQuickSave) btnQuickSave.style.display = 'none';
            if (adminPanel) adminPanel.classList.add('hidden');
            adminPin = "";
        }
        renderTemplateGrid();
    }

    function toggleAdminMode() {
        if (isAdminMode) {
            isAdminMode = false;
            if (adminTimeout) clearTimeout(adminTimeout);
            updateAdminUI();
            showToast(translations[currentLanguage]["toast_pin_exit"]);
        } else {
            openPinModal();
        }
    }

    function resetAdminTimeout() {
        if (adminTimeout) clearTimeout(adminTimeout);
        if (isAdminMode) {
            adminTimeout = setTimeout(() => {
                isAdminMode = false;
                updateAdminUI();
                showToast(translations[currentLanguage]["toast_pin_autolock"]);
            }, 5 * 60 * 1000);
        }
    }

    document.addEventListener('click', resetAdminTimeout);

    // --- PIN Verification Modal ---
    const pinModal = document.getElementById('pin-modal');
    const pinInput = document.getElementById('admin-pin-input');
    const pinErrorMsg = document.getElementById('pin-error-msg');
    
    function openPinModal() {
        pinInput.value = '';
        pinErrorMsg.classList.add('hidden');
        pinModal.classList.remove('hidden');
        pinInput.focus();
    }
    
    function closePinModal() {
        pinModal.classList.add('hidden');
    }
    
    async function verifyPin() {
        const pin = pinInput.value;
        if (!pin || pin.length < 4) return;
        
        try {
            const res = await fetch('/api/admin/verify', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ pin: pin })
            });
            if (res.ok) {
                isAdminMode = true;
                adminPin = pin;
                closePinModal();
                updateAdminUI();
                resetAdminTimeout();
                showToast(translations[currentLanguage]["toast_pin_success"]);
            } else {
                pinErrorMsg.classList.remove('hidden');
                pinInput.value = '';
                pinInput.focus();
            }
        } catch (e) {
            showToast('Network error verifying PIN', true);
        }
    }
    
    document.getElementById('btn-submit-pin').addEventListener('click', verifyPin);
    document.getElementById('btn-cancel-pin').addEventListener('click', closePinModal);
    pinInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') verifyPin();
    });
    document.getElementById('btn-admin-lock').addEventListener('click', toggleAdminMode);

    // --- Render Template Grid ---
    function renderTemplateGrid() {
        const grid = document.getElementById('templates-grid');
        if (!grid) return;
        grid.innerHTML = '';
        
        if (templates.length === 0) {
            grid.innerHTML = `
                <div class="empty-state" style="grid-column: 1/-1; text-align: center; color: var(--text-muted); padding: 3rem 0;">
                    ${translations[currentLanguage]["templates.empty_state"]}
                </div>
            `;
            return;
        }
        
        templates.forEach(tpl => {
            const card = document.createElement('div');
            card.className = `template-card ${activeTemplateId === tpl.id ? 'active-template' : ''}`;
            card.style.borderTop = `4px solid ${tpl.color || '#3b82f6'}`;
            
            let adminActionsHtml = '';
            if (isAdminMode) {
                adminActionsHtml = `
                    <div class="card-admin-actions">
                        <button class="btn-card-action btn-edit-tpl" data-id="${tpl.id}" title="Edit Template">✏️</button>
                        <button class="btn-card-action delete btn-delete-tpl" data-id="${tpl.id}" title="Delete Template">🗑️</button>
                    </div>
                `;
            }
            
            card.innerHTML = `
                ${adminActionsHtml}
                <div class="template-icon">${tpl.icon || '🖥️'}</div>
                <h3>${tpl.name}</h3>
                <p>${tpl.description || ''}</p>
            `;
            
            card.style.position = 'relative';
            if (activeTemplateId === tpl.id) {
                card.style.borderColor = 'var(--accent)';
            }
            
            card.addEventListener('click', (e) => {
                if (e.target.classList.contains('btn-card-action')) return;
                openConfirmModal(tpl);
            });
            
            grid.appendChild(card);
        });
        
        // Listeners for edit & delete buttons
        if (isAdminMode) {
            document.querySelectorAll('.btn-edit-tpl').forEach(btn => {
                btn.addEventListener('click', (e) => {
                    e.stopPropagation();
                    const id = parseInt(btn.dataset.id);
                    const tpl = templates.find(t => t.id === id);
                    if (tpl) openTemplateModal(tpl);
                });
            });
            
            document.querySelectorAll('.btn-delete-tpl').forEach(btn => {
                btn.addEventListener('click', (e) => {
                    e.stopPropagation();
                    const id = parseInt(btn.dataset.id);
                    const tpl = templates.find(t => t.id === id);
                    if (tpl) {
                        const confirmMsg = translations[currentLanguage]["confirm_del"].replace('{name}', tpl.name);
                        if (confirm(confirmMsg)) {
                            deleteTemplate(id);
                        }
                    }
                });
            });
        }
    }

    // --- Confirmation Modal Dialog ---
    const confirmModal = document.getElementById('confirm-modal');
    const confirmTitle = document.getElementById('confirm-title');
    const confirmMsg = document.getElementById('confirm-msg');
    const confirmSummary = document.getElementById('confirm-routing-summary');
    let confirmCallback = null;
    
    function openConfirmModal(template) {
        confirmTitle.textContent = `${translations[currentLanguage]["modal_confirm.title"]}: ${template.name}`;
        confirmMsg.textContent = translations[currentLanguage]["modal_confirm.subtitle"];
        
        confirmSummary.innerHTML = '';
        const encoders = devices.filter(d => d.role === 'encoder');
        const decoders = devices.filter(d => d.role === 'decoder');
        
        template.routing_map.forEach(item => {
            const enc = encoders.find(e => e.id === item.encoder_id);
            const encName = enc ? enc.name : `Input ${item.encoder_id}`;
            
            const decNames = item.decoder_ids.map(decId => {
                const dec = decoders.find(d => d.id === decId);
                return dec ? dec.name : `Output ${decId}`;
            }).join(', ');
            
            const row = document.createElement('div');
            row.className = 'confirm-route-item';
            row.innerHTML = `
                <span>${encName}</span>
                <span>➔ ${decNames}</span>
            `;
            confirmSummary.appendChild(row);
        });
        
        confirmCallback = () => {
            applyTemplate(template.id);
        };
        
        confirmModal.classList.remove('hidden');
    }
    
    document.getElementById('btn-submit-confirm').addEventListener('click', () => {
        if (confirmCallback) confirmCallback();
        confirmModal.classList.add('hidden');
    });
    
    document.getElementById('btn-cancel-confirm').addEventListener('click', () => {
        confirmModal.classList.add('hidden');
    });

    // --- Template Form Modals & Interactive Routing Editor ---
    const templateModal = document.getElementById('template-modal');
    const templateForm = document.getElementById('template-form');
    const routingRowsContainer = document.getElementById('routing-rows-container');
    
    document.getElementById('btn-new-template').addEventListener('click', () => openTemplateModal());
    document.getElementById('btn-cancel-template').addEventListener('click', closeTemplateModal);
    document.getElementById('btn-add-routing-row').addEventListener('click', () => addRoutingRow());
    
    templateForm.addEventListener('submit', (e) => {
        e.preventDefault();
        
        const id = document.getElementById('template-id').value;
        const name = document.getElementById('template-name').value;
        const desc = document.getElementById('template-desc').value;
        const color = document.getElementById('template-color').value;
        const icon = document.getElementById('template-icon').value;
        
        const routing_map = [];
        const rows = routingRowsContainer.querySelectorAll('.routing-row');
        
        rows.forEach(row => {
            const encoderSelect = row.querySelector('.encoder-select');
            const encId = encoderSelect.value;
            const checkedDecs = Array.from(row.querySelectorAll('.dropdown-item input:checked')).map(cb => cb.value);
            
            if (encId && checkedDecs.length > 0) {
                routing_map.push({
                    encoder_id: encId,
                    decoder_ids: checkedDecs
                });
            }
        });
        
        if (routing_map.length === 0) {
            showToast(translations[currentLanguage]["err_no_routes"], true);
            return;
        }
        
        saveTemplate({
            id: id ? parseInt(id) : null,
            name: name,
            description: desc,
            color: color,
            icon: icon,
            routing_map: routing_map
        });
    });
    
    function openTemplateModal(tpl = null) {
        templateForm.reset();
        document.getElementById('template-id').value = tpl ? tpl.id : '';
        
        const titleEl = document.getElementById('template-modal-title');
        if (titleEl) {
            titleEl.textContent = tpl 
                ? translations[currentLanguage]["modal_template.edit_title"] 
                : translations[currentLanguage]["modal_template.create_title"];
        }
        
        document.getElementById('template-name').value = tpl ? tpl.name : '';
        document.getElementById('template-desc').value = tpl ? tpl.description : '';
        document.getElementById('template-color').value = tpl ? tpl.color : '#3b82f6';
        document.getElementById('template-icon').value = tpl ? tpl.icon : '🖥️';
        
        routingRowsContainer.innerHTML = '';
        
        if (tpl && tpl.routing_map) {
            tpl.routing_map.forEach(item => {
                addRoutingRow(item.encoder_id, item.decoder_ids);
            });
        } else {
            addRoutingRow();
        }
        
        templateModal.classList.remove('hidden');
    }
    
    function closeTemplateModal() {
        templateModal.classList.add('hidden');
    }
    
    function addRoutingRow(selectedEncId = '', selectedDecIds = []) {
        const encoders = devices.filter(d => d.role === 'encoder');
        const decoders = devices.filter(d => d.role === 'decoder');
        
        if (encoders.length === 0 || decoders.length === 0) {
            showToast('No encoders or decoders available to configure', true);
            return;
        }
        
        const row = document.createElement('div');
        row.className = 'routing-row';
        
        let encOptions = encoders.map(enc => 
            `<option value="${enc.id}" ${enc.id === selectedEncId ? 'selected' : ''}>${enc.name} (ID: ${enc.id})</option>`
        ).join('');
        
        let decItems = decoders.map(dec => `
            <div class="dropdown-item" data-id="${dec.id}">
                <input type="checkbox" value="${dec.id}" id="dec-cb-${Math.random().toString(36).substr(2, 9)}" ${selectedDecIds.includes(dec.id) ? 'checked' : ''} style="width:auto; margin-right:8px;">
                <label style="display:inline; margin:0; cursor:pointer;">${dec.name}</label>
            </div>
        `).join('');
        
        const outputsLabel = currentLanguage === 'en' ? 'Select Outputs...' : 'เลือกเอาต์พุต...';
        const selectEncoderLabel = currentLanguage === 'en' ? 'Select Input...' : 'เลือกอินพุต...';
        
        row.innerHTML = `
            <select class="encoder-select" required>
                <option value="" disabled ${!selectedEncId ? 'selected' : ''}>${selectEncoderLabel}</option>
                ${encOptions}
            </select>
            
            <div class="decoders-checkbox-dropdown">
                <span class="dropdown-label">${outputsLabel}</span>
                <div class="dropdown-list">
                    ${decItems}
                </div>
            </div>
            
            <button type="button" class="btn-remove-row" title="Remove Route">✖</button>
        `;
        
        const dropdown = row.querySelector('.decoders-checkbox-dropdown');
        const label = dropdown.querySelector('.dropdown-label');
        
        function updateDropdownLabel() {
            const checked = Array.from(dropdown.querySelectorAll('input:checked'));
            if (checked.length === 0) {
                label.textContent = outputsLabel;
            } else if (checked.length === 1) {
                const decId = checked[0].value;
                const dec = decoders.find(d => d.id === decId);
                label.textContent = dec ? dec.name : `Decoder ${decId}`;
            } else {
                label.textContent = currentLanguage === 'en' 
                    ? `${checked.length} Outputs Selected` 
                    : `เลือกไว้ ${checked.length} จอ`;
            }
        }
        
        updateDropdownLabel();
        
        dropdown.addEventListener('click', (e) => {
            if (e.target === label || e.target === dropdown) {
                document.querySelectorAll('.decoders-checkbox-dropdown').forEach(d => {
                    if (d !== dropdown) d.classList.remove('open');
                });
                dropdown.classList.toggle('open');
            }
            e.stopPropagation();
        });
        
        dropdown.querySelector('.dropdown-list').addEventListener('click', (e) => {
            e.stopPropagation();
        });
        
        dropdown.querySelectorAll('input[type="checkbox"]').forEach(cb => {
            cb.addEventListener('change', updateDropdownLabel);
            const item = cb.closest('.dropdown-item');
            item.addEventListener('click', (e) => {
                if (e.target !== cb) {
                    cb.checked = !cb.checked;
                    updateDropdownLabel();
                }
            });
        });
        
        row.querySelector('.btn-remove-row').addEventListener('click', () => {
            row.remove();
        });
        
        routingRowsContainer.appendChild(row);
    }

    // --- Quick Save Current Layout Feature ---
    const btnQuickSave = document.getElementById('btn-quick-save');
    if (btnQuickSave) {
        btnQuickSave.addEventListener('click', () => {
            if (!isAdminMode) {
                showToast(currentLanguage === 'en' ? 'Please enter Admin Mode to Quick Save' : 'โปรดเข้าสู่โหมด Admin เพื่อใช้งาน Quick Save', true);
                openPinModal();
                return;
            }
            
            const decoders = devices.filter(d => d.role === 'decoder');
            const routing_map = [];
            
            const sourceGroups = {};
            decoders.forEach(dec => {
                const srcId = dec.source_id;
                if (srcId && srcId !== '' && srcId !== '0') {
                    if (!sourceGroups[srcId]) {
                        sourceGroups[srcId] = [];
                    }
                    sourceGroups[srcId].push(dec.id);
                }
            });
            
            for (const [encId, decIds] of Object.entries(sourceGroups)) {
                routing_map.push({
                    encoder_id: encId,
                    decoder_ids: decIds
                });
            }
            
            if (routing_map.length === 0) {
                showToast(translations[currentLanguage]["toast_quick_save_empty"], true);
                return;
            }
            
            openTemplateModal({
                id: null,
                name: currentLanguage === 'en' ? 'Quick Saved Preset' : 'บันทึกพรีเซ็ตด่วน',
                description: currentLanguage === 'en' ? 'Quick saved from matrix state' : 'บันทึกด่วนจากหน้า Matrix Router',
                color: '#10b981',
                icon: '📶',
                routing_map: routing_map
            });
        });
    }

    // ==========================================
    // --- ADMIN SYSTEM CONFIGURATION (PHASE 4) ---
    // ==========================================
    const adminConfigForm = document.getElementById('admin-config-form');
    if (adminConfigForm) {
        adminConfigForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const sysLangSelect = document.getElementById('config-sys-lang');
            const targetLang = sysLangSelect.value;
            
            try {
                const res = await fetch('/api/config', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-Admin-PIN': adminPin
                    },
                    body: JSON.stringify({ system_language: targetLang })
                });
                
                const data = await res.json();
                if (res.ok) {
                    showToast(translations[currentLanguage]["toast_config_update"]);
                    // Update client lang if it matches default system configuration update
                    changeLanguage(targetLang);
                } else {
                    showToast(data.error || 'Failed to update config', true);
                }
            } catch (e) {
                showToast('Network error saving settings', true);
            }
        });
    }

    const changePinForm = document.getElementById('change-pin-form');
    if (changePinForm) {
        changePinForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const oldPinInput = document.getElementById('pin-old');
            const newPinInput = document.getElementById('pin-new');
            
            const oldPin = oldPinInput.value;
            const newPin = newPinInput.value;
            
            if (oldPin !== adminPin) {
                showToast(currentLanguage === 'en' ? 'Incorrect current PIN' : 'รหัส PIN เดิมไม่ถูกต้อง', true);
                return;
            }
            
            try {
                const res = await fetch('/api/admin/change-pin', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ old_pin: oldPin, new_pin: newPin })
                });
                
                const data = await res.json();
                if (res.ok) {
                    showToast(translations[currentLanguage]["toast_pin_update"]);
                    adminPin = newPin; // update working local cache
                    oldPinInput.value = '';
                    newPinInput.value = '';
                } else {
                    showToast(data.error || 'Failed to change PIN', true);
                }
            } catch (e) {
                showToast('Network error changing PIN', true);
            }
        });
    }

    // Load initial system configuration
    async function loadSystemConfig() {
        try {
            const res = await fetch('/api/config');
            if (res.ok) {
                const config = await res.json();
                const sysLang = config.system_language || 'th';
                
                // Populate default select dropdown value in settings
                const sysLangSelect = document.getElementById('config-sys-lang');
                if (sysLangSelect) sysLangSelect.value = sysLang;
                
                // Choose language: localStorage takes precedence, then fallback to backend system language default
                const localLang = localStorage.getItem('metrix_language');
                const targetLang = localLang ? localLang : sysLang;
                
                applyLanguage(targetLang);
            }
        } catch (e) {
            console.error('Failed to load system config:', e);
            // Default fallback
            applyLanguage('th');
        }
    }

    // --- Init ---
    fetchDevices();
    loadSystemConfig();
});
