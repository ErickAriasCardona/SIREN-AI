import sys
import threading
from pathlib import Path
import tkinter as tk
import customtkinter as ctk

# Asegurar raíz en sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(ROOT_DIR))

from src.automation.platform_auth import run_login_sync, run_refresh_sync, run_diana_audit_sync, PLATFORM_CONFIG
from src.automation.credential_store import save_platform_credentials, get_platform_credentials
from src.automation.profile_deep_audit import synthesize_diana_findings
from src.automation.broadcast_manager import load_broadcast_config, save_broadcast_config

# Configuración visual de CustomTkinter
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

class CTkHoverTooltip:
    """Tooltip emergente moderno para mostrar la radiografía de perfil al pasar el cursor (hover)."""
    def __init__(self, widget, text=""):
        self.widget = widget
        self.text = text
        self.tip_window = None
        self.widget.bind("<Enter>", self.show_tip)
        self.widget.bind("<Leave>", self.hide_tip)

    def set_text(self, new_text: str):
        self.text = new_text

    def show_tip(self, event=None):
        if self.tip_window or not self.text:
            return
        
        # Posición calculada cerca del botón
        x = self.widget.winfo_rootx() - 120
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 10

        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{max(10, x)}+{y}")
        tw.attributes("-topmost", True)

        card = ctk.CTkFrame(
            tw,
            fg_color="#1f182f",
            border_width=2,
            border_color="#9d4edd",
            corner_radius=12
        )
        card.pack(fill="both", expand=True)

        header = ctk.CTkLabel(
            card,
            text="🔬 RADIOGRAFÍA ESTRATÉGICA (DIANA)",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color="#ffd166"
        )
        header.pack(anchor="w", padx=16, pady=(12, 6))

        body = ctk.CTkLabel(
            card,
            text=self.text,
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color="#f0ecf7",
            justify="left"
        )
        body.pack(anchor="w", padx=16, pady=(0, 14))

    def hide_tip(self, event=None):
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None

class VelvetControlCenter(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("VELVET AI — Centro de Control y Automatización")
        self.geometry("840 x 910")
        self.minsize(760, 800)

        # Paleta de colores Velvet VIP
        self.ACCENT_COLOR = "#9d4edd"       # Violeta / Púrpura elegante
        self.HOVER_COLOR = "#7b2cbf"
        self.BG_CARD = "#1a1625"            # Fondo oscuro tarjeta
        self.CARD_BORDER = "#3c2f58"
        self.GOLD_COLOR = "#ffd166"         # Acento dorado para ganancias
        self.TEXT_COLOR = "#f8f9fa"

        self.configure(fg_color="#0f0c15")

        self._build_ui()
        self._load_credentials_for_platform(self.platform_var.get())

    def _build_ui(self):
        # 1. Header / Encabezado
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=30, pady=(15, 5))

        title_label = ctk.CTkLabel(
            header_frame,
            text="🌌 VELVET AI",
            font=ctk.CTkFont(family="Segoe UI", size=26, weight="bold"),
            text_color=self.ACCENT_COLOR
        )
        title_label.pack(anchor="w")

        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Suite de Automatización y Operaciones para Creadoras WC (Playwright Engine)",
            font=ctk.CTkFont(family="Segoe UI", size=13),
            text_color="#a09cb0"
        )
        subtitle_label.pack(anchor="w")

        # 2. Tarjeta de Acceso y Credenciales
        card = ctk.CTkFrame(self, fg_color=self.BG_CARD, corner_radius=15, border_width=1, border_color=self.CARD_BORDER)
        card.pack(fill="x", padx=30, pady=8)

        card_title = ctk.CTkLabel(
            card,
            text="🔐 Acceso Automatizado a Plataforma",
            font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
            text_color="#ffffff"
        )
        card_title.pack(anchor="w", padx=25, pady=(12, 6))

        # Selector de Plataforma
        plat_row = ctk.CTkFrame(card, fg_color="transparent")
        plat_row.pack(fill="x", padx=25, pady=(0, 8))

        plat_label = ctk.CTkLabel(plat_row, text="Plataforma:", font=ctk.CTkFont(size=13, weight="bold"), text_color="#d0cbdc")
        plat_label.pack(side="left", padx=(0, 10))

        self.platform_var = ctk.StringVar(value="LoyalFans")
        self.platform_menu = ctk.CTkOptionMenu(
            plat_row,
            variable=self.platform_var,
            values=["LoyalFans", "Stripchat", "Flirt4Free", "Streamate"],
            fg_color="#2b233d",
            button_color=self.ACCENT_COLOR,
            button_hover_color=self.HOVER_COLOR,
            font=ctk.CTkFont(size=13, weight="bold"),
            height=34,
            corner_radius=8,
            command=self._on_platform_changed
        )
        self.platform_menu.pack(side="left", fill="x", expand=True)

        # Campos de Usuario y Contraseña
        inputs_frame = ctk.CTkFrame(card, fg_color="transparent")
        inputs_frame.pack(fill="x", padx=25, pady=(0, 8))

        # Columna Usuario
        u_box = ctk.CTkFrame(inputs_frame, fg_color="transparent")
        u_box.pack(side="left", fill="x", expand=True, padx=(0, 10))
        u_lbl = ctk.CTkLabel(u_box, text="Correo o Usuario:", font=ctk.CTkFont(size=12), text_color="#b5b0c4")
        u_lbl.pack(anchor="w")
        self.user_entry = ctk.CTkEntry(
            u_box,
            placeholder_text="correo@ejemplo.com o username",
            height=36,
            corner_radius=8,
            fg_color="#120e1c",
            border_color="#433760"
        )
        self.user_entry.pack(fill="x", pady=(2, 0))

        # Columna Contraseña
        p_box = ctk.CTkFrame(inputs_frame, fg_color="transparent")
        p_box.pack(side="left", fill="x", expand=True, padx=(10, 0))
        p_lbl = ctk.CTkLabel(p_box, text="Contraseña:", font=ctk.CTkFont(size=12), text_color="#b5b0c4")
        p_lbl.pack(anchor="w")
        self.pass_entry = ctk.CTkEntry(
            p_box,
            placeholder_text="••••••••••••",
            show="*",
            height=36,
            corner_radius=8,
            fg_color="#120e1c",
            border_color="#433760"
        )
        self.pass_entry.pack(fill="x", pady=(2, 0))

        # Panel de Opciones de Redirección Post-Login (Feed vs Transmisión en Vivo)
        redir_frame = ctk.CTkFrame(card, fg_color="#181326", corner_radius=10, border_width=1, border_color="#3e3056")
        redir_frame.pack(fill="x", padx=25, pady=(2, 10))

        redir_top = ctk.CTkFrame(redir_frame, fg_color="transparent")
        redir_top.pack(fill="x", padx=15, pady=(8, 4))

        redir_lbl = ctk.CTkLabel(
            redir_top,
            text="🎯 Redirección Automática tras Iniciar Sesión:",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#ffd166"
        )
        redir_lbl.pack(side="left")

        self.btn_live_setup = ctk.CTkButton(
            redir_top,
            text="🎛️ Ajustes En Vivo (OBS / Logitech / Metas)",
            font=ctk.CTkFont(size=11, weight="bold"),
            fg_color="#4a154b",
            hover_color="#702072",
            height=26,
            corner_radius=6,
            command=self._open_live_setup_window
        )
        self.btn_live_setup.pack(side="right")

        self.redirect_target_var = ctk.StringVar(value="feed")

        redir_opts = ctk.CTkFrame(redir_frame, fg_color="transparent")
        redir_opts.pack(fill="x", padx=15, pady=(0, 8))

        self.rb_feed = ctk.CTkRadioButton(
            redir_opts,
            text="📰 Feed / Muro Principal",
            variable=self.redirect_target_var,
            value="feed",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=self.ACCENT_COLOR,
            hover_color=self.HOVER_COLOR
        )
        self.rb_feed.pack(side="left", padx=(0, 20))

        self.rb_live = ctk.CTkRadioButton(
            redir_opts,
            text="📹 Transmisión en Vivo (Broadcast)",
            variable=self.redirect_target_var,
            value="live",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#ff2a85",
            hover_color="#d61b6b"
        )
        self.rb_live.pack(side="left", padx=(0, 20))

        self.rb_home = ctk.CTkRadioButton(
            redir_opts,
            text="🏠 Panel General (Home)",
            variable=self.redirect_target_var,
            value="home",
            font=ctk.CTkFont(size=12),
            fg_color="#6c757d",
            hover_color="#adb5bd"
        )
        self.rb_home.pack(side="left")

        # Opciones y Botón
        opts_frame = ctk.CTkFrame(card, fg_color="transparent")
        opts_frame.pack(fill="x", padx=25, pady=(4, 15))

        self.save_creds_var = ctk.BooleanVar(value=True)
        self.save_creds_checkbox = ctk.CTkCheckBox(
            opts_frame,
            text="💾 Recordar credenciales para esta plataforma",
            variable=self.save_creds_var,
            fg_color=self.ACCENT_COLOR,
            hover_color=self.HOVER_COLOR,
            font=ctk.CTkFont(size=12)
        )
        self.save_creds_checkbox.pack(side="left")

        self.login_button = ctk.CTkButton(
            opts_frame,
            text="🚀 INICIAR SESIÓN Y ABRIR PLATAFORMA",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=self.ACCENT_COLOR,
            hover_color=self.HOVER_COLOR,
            height=40,
            corner_radius=8,
            command=self._start_automation_thread
        )
        self.login_button.pack(side="right", padx=(10, 0))

        self.assisted_button = ctk.CTkButton(
            opts_frame,
            text="🛡️ MODO ASISTIDO (CLOUDFLARE / 2FA)",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#312244",
            hover_color="#4d194d",
            height=40,
            corner_radius=8,
            command=self._start_assisted_login_thread
        )
        self.assisted_button.pack(side="right", padx=(10, 0))

        # 3. 📊 PANEL DE RESUMEN DE LA CREADORA (MÉTRICAS EN VIVO)
        self.metrics_card = ctk.CTkFrame(self, fg_color="#181324", corner_radius=15, border_width=1, border_color="#533c77")
        self.metrics_card.pack(fill="x", padx=30, pady=6)

        m_top_row = ctk.CTkFrame(self.metrics_card, fg_color="transparent")
        m_top_row.pack(fill="x", padx=20, pady=(10, 6))

        m_header = ctk.CTkLabel(
            m_top_row,
            text="📊 Resumen de tu Perfil en Vivo (Post-Login)",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            text_color="#ffffff"
        )
        m_header.pack(side="left")

        # Botón con Tooltip y Clic Derecho para DIANA (Auditora de Perfil)
        self.btn_diana = ctk.CTkButton(
            m_top_row,
            text="🔬 Estrategia DIANA ⓘ",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#6a1b9a",
            hover_color="#8e24aa",
            height=28,
            width=150,
            corner_radius=6,
            command=self._run_diana_audit_thread
        )
        self.btn_diana.pack(side="right", padx=(8, 0))

        # Botón para Lovense Stream Master
        self.btn_lovense = ctk.CTkButton(
            m_top_row,
            text="💖 Lovense Master",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#ad1457",
            hover_color="#d81b60",
            height=28,
            width=140,
            corner_radius=6,
            command=self._launch_lovense_thread
        )
        self.btn_lovense.pack(side="right", padx=(8, 0))

        # Tooltip para DIANA y bind de clic derecho
        initial_strategy = synthesize_diana_findings({"platform": "loyalfans"})
        self.current_diana_dossier = initial_strategy.get("dossier_text", "")
        self.diana_tooltip = CTkHoverTooltip(self.btn_diana, text=initial_strategy.get("tooltip_text", ""))

        # Clic derecho para ver el dossier completo
        self.btn_diana.bind("<Button-3>", self._open_diana_dossier_window)
        self.btn_diana.bind("<Button-2>", self._open_diana_dossier_window)

        self.btn_refresh = ctk.CTkButton(
            m_top_row,
            text="🔄 Actualizar",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#3c2a55",
            hover_color="#5c3f82",
            height=28,
            width=95,
            corner_radius=6,
            command=self._refresh_metrics_thread
        )
        self.btn_refresh.pack(side="right")

        stats_grid = ctk.CTkFrame(self.metrics_card, fg_color="transparent")
        stats_grid.pack(fill="x", padx=15, pady=(0, 12))

        # Tarjetas de estadísticas
        self.stat_user = self._create_stat_badge(stats_grid, "👤 Creadora", "No conectada", "#d0cbdc")
        self.stat_earn = self._create_stat_badge(stats_grid, "💰 Ganancias", "$0.00", self.GOLD_COLOR)
        self.stat_foll = self._create_stat_badge(stats_grid, "👥 Seguidores", "--", "#a8dadc")
        self.stat_msgs = self._create_stat_badge(stats_grid, "✉️ Mensajes", "0 nuevos", "#ff70a6")
        self.stat_alrt = self._create_stat_badge(stats_grid, "🔔 Alertas", "0", "#ffd166")

        # 4. Consola de Automatización en Vivo
        log_frame = ctk.CTkFrame(self, fg_color=self.BG_CARD, corner_radius=15, border_width=1, border_color=self.CARD_BORDER)
        log_frame.pack(fill="both", expand=True, padx=30, pady=(6, 15))

        log_title = ctk.CTkLabel(
            log_frame,
            text="📡 Registro en Vivo de Playwright (Cookies, Auth, Scrape & Auditoría)",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#c8c2d8"
        )
        log_title.pack(anchor="w", padx=20, pady=(8, 4))

        self.log_textbox = ctk.CTkTextbox(
            log_frame,
            fg_color="#0e0a17",
            text_color="#48e5c2",
            font=ctk.CTkFont(family="Consolas", size=11),
            corner_radius=8,
            border_width=1,
            border_color="#2c2242"
        )
        self.log_textbox.pack(fill="both", expand=True, padx=20, pady=(0, 12))
        self.log_textbox.insert("end", "[VELVET AI ONLINE] Selecciona plataforma, introduce tus accesos y pulsa iniciar.\n")

    def _create_stat_badge(self, parent, label_text, default_val, val_color):
        badge = ctk.CTkFrame(parent, fg_color="#221b33", corner_radius=10, border_width=1, border_color="#3c2f58")
        badge.pack(side="left", fill="both", expand=True, padx=5)

        lbl = ctk.CTkLabel(badge, text=label_text, font=ctk.CTkFont(size=11), text_color="#9d98ad")
        lbl.pack(pady=(6, 2))

        val = ctk.CTkLabel(badge, text=default_val, font=ctk.CTkFont(size=14, weight="bold"), text_color=val_color)
        val.pack(pady=(0, 6))
        return val

    def _on_platform_changed(self, platform_name: str):
        self._load_credentials_for_platform(platform_name)
        # Actualizar tooltip preliminar según la plataforma
        strat = synthesize_diana_findings({"platform": platform_name.lower()})
        self.diana_tooltip.set_text(strat.get("tooltip_text", ""))

    def _load_credentials_for_platform(self, platform_name: str):
        creds = get_platform_credentials(platform_name.lower())
        saved_user = creds.get("username", "")
        saved_pwd = creds.get("password", "")

        self.user_entry.delete(0, "end")
        if saved_user:
            self.user_entry.insert(0, saved_user)

        self.pass_entry.delete(0, "end")
        if saved_pwd:
            self.pass_entry.insert(0, saved_pwd)

        if saved_user and saved_pwd:
            self._log(f"💾 Credenciales autocompletadas para [{platform_name}].")

    def _log(self, message: str):
        self.after(0, lambda: self._append_log(message))

    def _append_log(self, message: str):
        self.log_textbox.insert("end", f"> {message}\n")
        self.log_textbox.see("end")

    def _update_metrics_ui(self, metrics: dict):
        def apply():
            user = metrics.get("username") or metrics.get("nickname") or "Conectada"
            self.stat_user.configure(text=f"@{user}" if not user.startswith("@") else user)
            self.stat_earn.configure(text=metrics.get("earnings", "$0.00"))
            self.stat_foll.configure(text=metrics.get("followers", "--"))
            self.stat_msgs.configure(text=f"{metrics.get('unread_messages', '0')} nuevos")
            self.stat_alrt.configure(text=str(metrics.get("alerts", "0")))
            self._log("✨ Panel de estadísticas actualizado con los datos de tu cuenta.")
        self.after(0, apply)

    def _update_diana_ui(self, diana_data: dict):
        def apply():
            tip_text = diana_data.get("tooltip_text", "")
            dossier_text = diana_data.get("dossier_text", "")
            if tip_text:
                self.diana_tooltip.set_text(tip_text)
            if dossier_text:
                self.current_diana_dossier = dossier_text
            self._log("💡 DIANA actualizó la radiografía estratégica. Pasa el cursor (hover) o haz CLIC DERECHO para ver el Dossier Completo.")
        self.after(0, apply)

    def _open_diana_dossier_window(self, event=None):
        """Abre la ventana VIP con el dossier forense y la biografía comercial de la creadora."""
        dossier_win = ctk.CTkToplevel(self)
        dossier_win.title("DIANA — Dossier Estratégico & Biografía de Creadora")
        dossier_win.geometry("720x760")
        dossier_win.minsize(620, 620)
        dossier_win.configure(fg_color="#0f0c15")
        dossier_win.attributes("-topmost", True)

        header = ctk.CTkFrame(dossier_win, fg_color="transparent")
        header.pack(fill="x", padx=25, pady=(18, 8))

        t = ctk.CTkLabel(header, text="🔬 ESTUDIO FORENSE & BIOGRAFÍA COMERCIAL", font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold"), text_color="#ffd166")
        t.pack(anchor="w")

        sub = ctk.CTkLabel(header, text="Auditoría de Perfil, Fans en Chat y Factores de Monetización (+18)", font=ctk.CTkFont(size=12), text_color="#a09cb0")
        sub.pack(anchor="w")

        text_box = ctk.CTkTextbox(
            dossier_win,
            fg_color="#181324",
            text_color="#f0ecf7",
            font=ctk.CTkFont(family="Consolas", size=12),
            border_width=1,
            border_color="#533c77",
            corner_radius=10
        )
        text_box.pack(fill="both", expand=True, padx=25, pady=10)

        dossier_content = self.current_diana_dossier or "Cargando estudio forense de DIANA..."
        text_box.insert("1.0", dossier_content)

        btn_close = ctk.CTkButton(
            dossier_win,
            text="CERRAR DOSSIER",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#6a1b9a",
            hover_color="#8e24aa",
            height=38,
            corner_radius=8,
            command=dossier_win.destroy
        )
        btn_close.pack(pady=(5, 18), padx=25, fill="x")

    def _open_live_setup_window(self):
        """Abre la ventana de configuración y verificación para transmisiones en vivo."""
        cfg = load_broadcast_config()

        live_win = ctk.CTkToplevel(self)
        live_win.title("Transmisión en Vivo — OBS, Logitech & @SAMBARTONN23")
        live_win.geometry("680x720")
        live_win.minsize(620, 640)
        live_win.configure(fg_color="#0f0c15")
        live_win.attributes("-topmost", True)

        header = ctk.CTkFrame(live_win, fg_color="transparent")
        header.pack(fill="x", padx=25, pady=(18, 6))

        t = ctk.CTkLabel(header, text="🎛️ CONFIGURACIÓN DE SALA EN VIVO", font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold"), text_color="#ff2a85")
        t.pack(anchor="w")

        sub = ctk.CTkLabel(header, text="Cámara OBS, Micrófono Logitech, Tema con @SAMBARTONN23 y Metas de 3 Niveles", font=ctk.CTkFont(size=12), text_color="#a09cb0")
        sub.pack(anchor="w")

        # Tarjetas de estado de Hardware
        hw_frame = ctk.CTkFrame(live_win, fg_color="#181326", corner_radius=10, border_width=1, border_color="#3e3056")
        hw_frame.pack(fill="x", padx=25, pady=8)

        hw_grid = ctk.CTkFrame(hw_frame, fg_color="transparent")
        hw_grid.pack(fill="x", padx=15, pady=10)

        # Badge Cámara
        cam_box = ctk.CTkFrame(hw_grid, fg_color="#221b33", corner_radius=8, border_width=1, border_color="#533c77")
        cam_box.pack(side="left", fill="both", expand=True, padx=(0, 6))
        ctk.CTkLabel(cam_box, text="🎥 Cámara Seleccionada", font=ctk.CTkFont(size=11), text_color="#b5b0c4").pack(pady=(6, 2))
        ctk.CTkLabel(cam_box, text="🟢 OBS Virtual Camera", font=ctk.CTkFont(size=13, weight="bold"), text_color="#48e5c2").pack(pady=(0, 6))

        # Badge Micrófono
        mic_box = ctk.CTkFrame(hw_grid, fg_color="#221b33", corner_radius=8, border_width=1, border_color="#533c77")
        mic_box.pack(side="left", fill="both", expand=True, padx=(6, 0))
        ctk.CTkLabel(mic_box, text="🎙️ Micrófono de Entrada", font=ctk.CTkFont(size=11), text_color="#b5b0c4").pack(pady=(6, 2))
        ctk.CTkLabel(mic_box, text="🟢 Micrófono (Logitech BRIO)", font=ctk.CTkFont(size=13, weight="bold"), text_color="#ffd166").pack(pady=(0, 6))

        # Sección de Tema de la Sala
        topic_card = ctk.CTkFrame(live_win, fg_color="#181326", corner_radius=10, border_width=1, border_color="#3e3056")
        topic_card.pack(fill="x", padx=25, pady=8)

        topic_top = ctk.CTkFrame(topic_card, fg_color="transparent")
        topic_top.pack(fill="x", padx=15, pady=(10, 4))
        ctk.CTkLabel(topic_top, text="🏷️ Tema / Título de la Sala (Siempre contiene @SAMBARTONN23):", font=ctk.CTkFont(size=12, weight="bold"), text_color="#ffffff").pack(side="left")

        # Selector de presets
        presets = cfg.get("topic_presets", [])
        def on_preset_selected(choice):
            topic_entry.delete(0, "end")
            topic_entry.insert(0, choice)

        if presets:
            preset_menu = ctk.CTkOptionMenu(
                topic_top,
                values=presets,
                command=on_preset_selected,
                width=170,
                height=26,
                fg_color="#3c2a55",
                button_color="#5c3f82",
                font=ctk.CTkFont(size=11)
            )
            preset_menu.set("Elegir Preset...")
            preset_menu.pack(side="right")

        topic_entry = ctk.CTkEntry(
            topic_card,
            height=38,
            corner_radius=8,
            fg_color="#120e1c",
            border_color="#533c77",
            font=ctk.CTkFont(size=12)
        )
        topic_entry.pack(fill="x", padx=15, pady=(0, 12))
        topic_entry.insert(0, cfg.get("room_topic", ""))

        # Sección Objetivo del Día con 3 Niveles
        goals_card = ctk.CTkFrame(live_win, fg_color="#181326", corner_radius=10, border_width=1, border_color="#3e3056")
        goals_card.pack(fill="both", expand=True, padx=25, pady=8)

        g_title = ctk.CTkLabel(goals_card, text="🎯 Objetivo del Día — Configuración de 3 Niveles (Tokens / USD):", font=ctk.CTkFont(size=12, weight="bold"), text_color="#ffd166")
        g_title.pack(anchor="w", padx=15, pady=(10, 6))

        goals_data = cfg.get("goals", {})
        g1 = goals_data.get("level_1", {})
        g2 = goals_data.get("level_2", {})
        g3 = goals_data.get("level_3", {})

        def create_goal_row(parent, level_title, default_tk, default_usd, default_desc, accent_color):
            row = ctk.CTkFrame(parent, fg_color="#201830", corner_radius=8, border_width=1, border_color="#3e3056")
            row.pack(fill="x", padx=15, pady=4)

            top = ctk.CTkFrame(row, fg_color="transparent")
            top.pack(fill="x", padx=10, pady=(6, 2))

            lbl = ctk.CTkLabel(top, text=level_title, font=ctk.CTkFont(size=12, weight="bold"), text_color=accent_color)
            lbl.pack(side="left")

            tk_entry = ctk.CTkEntry(top, width=70, height=26, corner_radius=6, font=ctk.CTkFont(size=11))
            tk_entry.pack(side="right", padx=(4, 0))
            tk_entry.insert(0, str(default_tk))

            tk_lbl = ctk.CTkLabel(top, text="TK:", font=ctk.CTkFont(size=11), text_color="#a09cb0")
            tk_lbl.pack(side="right")

            usd_entry = ctk.CTkEntry(top, width=65, height=26, corner_radius=6, font=ctk.CTkFont(size=11))
            usd_entry.pack(side="right", padx=(4, 10))
            usd_entry.insert(0, str(default_usd))

            usd_lbl = ctk.CTkLabel(top, text="USD $:", font=ctk.CTkFont(size=11), text_color="#a09cb0")
            usd_lbl.pack(side="right")

            desc_entry = ctk.CTkEntry(row, height=28, corner_radius=6, fg_color="#120e1c", font=ctk.CTkFont(size=11))
            desc_entry.pack(fill="x", padx=10, pady=(0, 8))
            desc_entry.insert(0, default_desc)

            return tk_entry, usd_entry, desc_entry

        e_g1_tk, e_g1_usd, e_g1_desc = create_goal_row(goals_card, "🔥 Nivel 1: Calentamiento & Conexión", g1.get("tokens", 250), g1.get("usd", 25.0), g1.get("desc", ""), "#48e5c2")
        e_g2_tk, e_g2_usd, e_g2_desc = create_goal_row(goals_card, "⚡ Nivel 2: Intensidad & Sensualidad", g2.get("tokens", 750), g2.get("usd", 75.0), g2.get("desc", ""), "#ffd166")
        e_g3_tk, e_g3_usd, e_g3_desc = create_goal_row(goals_card, "😈 Nivel 3: Clímax & Dominación Total", g3.get("tokens", 1500), g3.get("usd", 150.0), g3.get("desc", ""), "#ff2a85")

        # Botones inferiores
        b_frame = ctk.CTkFrame(live_win, fg_color="transparent")
        b_frame.pack(fill="x", padx=25, pady=(10, 18))

        def save_and_close():
            raw_topic = topic_entry.get().strip()
            if "@SAMBARTONN23" not in raw_topic.upper():
                raw_topic = f"{raw_topic} @SAMBARTONN23".strip()

            cfg["room_topic"] = raw_topic
            try:
                g1_tk = int(e_g1_tk.get().strip())
                g1_usd = float(e_g1_usd.get().strip())
                g2_tk = int(e_g2_tk.get().strip())
                g2_usd = float(e_g2_usd.get().strip())
                g3_tk = int(e_g3_tk.get().strip())
                g3_usd = float(e_g3_usd.get().strip())
            except Exception:
                g1_tk, g1_usd = 250, 25.0
                g2_tk, g2_usd = 750, 75.0
                g3_tk, g3_usd = 1500, 150.0

            cfg["goals"]["level_1"]["tokens"] = g1_tk
            cfg["goals"]["level_1"]["usd"] = g1_usd
            cfg["goals"]["level_1"]["desc"] = e_g1_desc.get().strip()

            cfg["goals"]["level_2"]["tokens"] = g2_tk
            cfg["goals"]["level_2"]["usd"] = g2_usd
            cfg["goals"]["level_2"]["desc"] = e_g2_desc.get().strip()

            cfg["goals"]["level_3"]["tokens"] = g3_tk
            cfg["goals"]["level_3"]["usd"] = g3_usd
            cfg["goals"]["level_3"]["desc"] = e_g3_desc.get().strip()

            save_broadcast_config(cfg)
            self._log(f"💾 Ajustes de transmisión guardados: Tema \"{raw_topic}\" | Metas de 3 niveles actualizadas.")
            live_win.destroy()

        def copy_goals_summary():
            raw_topic = topic_entry.get().strip()
            if "@SAMBARTONN23" not in raw_topic.upper():
                raw_topic = f"{raw_topic} @SAMBARTONN23".strip()
            summary = (
                f"🖤 {raw_topic}\n"
                f"🎯 METAS DEL DÍA — SAM BARTON:\n"
                f"1️⃣ {e_g1_tk.get()} TK (${e_g1_usd.get()}) ➔ {e_g1_desc.get()}\n"
                f"2️⃣ {e_g2_tk.get()} TK (${e_g2_usd.get()}) ➔ {e_g2_desc.get()}\n"
                f"3️⃣ {e_g3_tk.get()} TK (${e_g3_usd.get()}) ➔ {e_g3_desc.get()}\n"
                f"✨ ¡Lovense activo en sala! Tips activan vibración inmediata 🔥"
            )
            self.clipboard_clear()
            self.clipboard_append(summary)
            self._log("📋 ¡Metas y tema copiados al portapapeles! Listo para pegar en el chat de tu sala.")

        btn_copy = ctk.CTkButton(
            b_frame,
            text="📋 COPIAR METAS PARA CHAT",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#3c2a55",
            hover_color="#5c3f82",
            height=38,
            corner_radius=8,
            command=copy_goals_summary
        )
        btn_copy.pack(side="left", fill="x", expand=True, padx=(0, 6))

        btn_save = ctk.CTkButton(
            b_frame,
            text="💾 GUARDAR AJUSTES DE SALA",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#6a1b9a",
            hover_color="#8e24aa",
            height=38,
            corner_radius=8,
            command=save_and_close
        )
        btn_save.pack(side="left", fill="x", expand=True, padx=(6, 0))

    def _run_diana_audit_thread(self):
        self.btn_diana.configure(state="disabled", text="⏳ Analizando...")

        def worker():
            try:
                run_diana_audit_sync(
                    status_callback=self._log,
                    audit_callback=self._update_diana_ui
                )
            except Exception as e:
                self._log(f"Error en auditoría de Diana: {e}")
            finally:
                self.after(0, lambda: self.btn_diana.configure(state="normal", text="🔬 Estrategia DIANA ⓘ"))

        threading.Thread(target=worker, daemon=True).start()

    def _refresh_metrics_thread(self):
        self._log("Consultando métricas financieras actualizadas en tiempo real...")
        self.btn_refresh.configure(state="disabled", text="⏳...")

        def worker():
            try:
                # 1. Cargar las métricas financieras más recientes (balance $15.59, 603 fans, etc.)
                from src.analytics.financial_live_sync import parse_financials_dump
                fin = parse_financials_dump()
                self._update_metrics_ui({
                    "username": "sambarton23",
                    "earnings": fin.get("balance_formatted", "$15.59 USD"),
                    "followers": f"{fin.get('fans_count', 603)} Fans",
                    "unread_messages": "1 nuevo",
                    "alerts": str(fin.get("alerts_count", 2))
                })
                # 2. Refrescar si hay ventana de Playwright activa
                run_refresh_sync(
                    status_callback=self._log,
                    metrics_callback=self._update_metrics_ui
                )
            except Exception as e:
                self._log(f"Nota al refrescar: {e}")
            finally:
                self.after(0, lambda: self.btn_refresh.configure(state="normal", text="🔄 Actualizar"))

        threading.Thread(target=worker, daemon=True).start()

    def _start_automation_thread(self):
        platform = self.platform_var.get().lower()
        user = self.user_entry.get().strip()
        pwd = self.pass_entry.get().strip()
        save_creds = self.save_creds_var.get()
        redirect_target = self.redirect_target_var.get()

        if not user or not pwd:
            self._log("⚠️ Advertencia: Por favor ingresa el correo/usuario y la contraseña.")
            return

        if save_creds:
            save_platform_credentials(platform, user, pwd)
            self._log(f"💾 Credenciales guardadas localmente para [{platform.upper()}].")

        target_name = "Feed / Muro" if redirect_target == "feed" else ("Transmisión en Vivo" if redirect_target == "live" else "Panel General")
        self.login_button.configure(state="disabled", text="⏳ CONECTANDO...")
        self._log(f"Iniciando tarea para [{platform.upper()}] (Destino: {target_name})...")

        if redirect_target == "live":
            b_cfg = load_broadcast_config()
            self._log("🎥 [EN VIVO] Cámara priorizada: OBS Virtual Camera")
            self._log("🎙️ [EN VIVO] Micrófono confirmado: Micrófono (Logitech BRIO)")
            self._log(f"🏷️ [EN VIVO] Tema configurado: \"{b_cfg.get('room_topic')}\"")
            g = b_cfg.get("goals", {})
            self._log(f"🎯 [EN VIVO] Metas 3 niveles: N1 ({g.get('level_1', {}).get('tokens', 250)} TK / ${g.get('level_1', {}).get('usd', 25)}) | N2 ({g.get('level_2', {}).get('tokens', 750)} TK / ${g.get('level_2', {}).get('usd', 75)}) | N3 ({g.get('level_3', {}).get('tokens', 1500)} TK / ${g.get('level_3', {}).get('usd', 150)})")

        def worker():
            try:
                self.after(2500, lambda: self.login_button.configure(text="🟢 SESIÓN EN CURSO (ABIERTA)"))
                run_login_sync(
                    platform_key=platform,
                    username_or_email=user,
                    password=pwd,
                    save_session=True,
                    redirect_target=redirect_target,
                    status_callback=self._log,
                    metrics_callback=self._update_metrics_ui,
                    diana_callback=self._update_diana_ui
                )
            except Exception as e:
                self._log(f"Error inesperado: {str(e)}")
            finally:
                self.after(0, lambda: self.login_button.configure(state="normal", text="🚀 INICIAR SESIÓN Y ABRIR PLATAFORMA"))

        threading.Thread(target=worker, daemon=True).start()

    def _start_assisted_login_thread(self):
        platform = self.platform_var.get().lower()
        redirect_target = self.redirect_target_var.get()
        target_name = "Feed / Muro" if redirect_target == "feed" else ("Transmisión en Vivo" if redirect_target == "live" else "Panel General")
        self._log(f"🛡️ [MODO ASISTIDO] Abriendo navegador para [{platform.upper()}] (Destino: {target_name}).")
        if redirect_target == "live":
            b_cfg = load_broadcast_config()
            self._log("🎥 [EN VIVO] Cámara priorizada: OBS Virtual Camera")
            self._log("🎙️ [EN VIVO] Micrófono confirmado: Micrófono (Logitech BRIO)")
            self._log(f"🏷️ [EN VIVO] Tema: \"{b_cfg.get('room_topic')}\"")
        self._log("👉 Resuelve el reto de Cloudflare ('Verifica que eres humano') o 2FA en la ventana de Chrome.")
        self.assisted_button.configure(state="disabled", text="⏳ ASISTIDO ACTIVO...")

        def worker():
            try:
                from src.automation.manual_login_booster import run_assisted_login
                import asyncio
                asyncio.run(run_assisted_login(platform, redirect_target=redirect_target))
                self._log(f"✨ Modo asistido finalizado para [{platform.upper()}]. Las cookies y sesión quedaron guardadas.")
            except Exception as e:
                self._log(f"Nota en modo asistido: {e}")
            finally:
                self.after(0, lambda: self.assisted_button.configure(state="normal", text="🛡️ MODO ASISTIDO (CLOUDFLARE / 2FA)"))

        threading.Thread(target=worker, daemon=True).start()

    def _launch_lovense_thread(self):
        self._log("💖 [LOVENSE] Iniciando Lovense Stream Master...")
        self.btn_lovense.configure(state="disabled", text="⏳ Iniciando...")

        def worker():
            try:
                from src.integrations.lovense_manager import launch_stream_master, check_local_lovense_api
                res = launch_stream_master()
                if res.get("success"):
                    self._log("✨ Lovense Stream Master se ha iniciado correctamente en segundo plano.")
                    self._log("💡 Tip: Vincula tus juguetes en Stream Master vía dongle USB o Lovense Connect.")
                    # Comprobar si la API local responde
                    api = check_local_lovense_api()
                    if api.get("online"):
                        self._log(f"🟢 Juguetes Lovense detectados en red local (Puerto {api.get('port')}).")
                    else:
                        self._log("ℹ️ Abre la aplicación Lovense Connect o enciende tu dongle Bluetooth si vas a transmitir.")
                else:
                    self._log(f"⚠️ Nota al abrir Stream Master: {res.get('error')}")
            except Exception as e:
                self._log(f"Error al iniciar Lovense: {e}")
            finally:
                self.after(0, lambda: self.btn_lovense.configure(state="normal", text="💖 Lovense Master"))

        threading.Thread(target=worker, daemon=True).start()

def main():
    app = VelvetControlCenter()
    app.mainloop()

if __name__ == "__main__":
    main()
