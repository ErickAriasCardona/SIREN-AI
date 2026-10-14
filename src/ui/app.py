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
        self._log("Consultando métricas actualizadas del navegador...")
        self.btn_refresh.configure(state="disabled", text="⏳...")

        def worker():
            try:
                run_refresh_sync(
                    status_callback=self._log,
                    metrics_callback=self._update_metrics_ui
                )
            except Exception as e:
                self._log(f"Error al refrescar métricas: {e}")
            finally:
                self.after(0, lambda: self.btn_refresh.configure(state="normal", text="🔄 Actualizar"))

        threading.Thread(target=worker, daemon=True).start()

    def _start_automation_thread(self):
        platform = self.platform_var.get().lower()
        user = self.user_entry.get().strip()
        pwd = self.pass_entry.get().strip()
        save_creds = self.save_creds_var.get()

        if not user or not pwd:
            self._log("⚠️ Advertencia: Por favor ingresa el correo/usuario y la contraseña.")
            return

        if save_creds:
            save_platform_credentials(platform, user, pwd)
            self._log(f"💾 Credenciales guardadas localmente para [{platform.upper()}].")

        self.login_button.configure(state="disabled", text="⏳ CONECTANDO...")
        self._log(f"Iniciando tarea para [{platform.upper()}]...")

        def worker():
            try:
                self.after(2500, lambda: self.login_button.configure(text="🟢 SESIÓN EN CURSO (ABIERTA)"))
                run_login_sync(
                    platform_key=platform,
                    username_or_email=user,
                    password=pwd,
                    save_session=True,
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
        self._log(f"🛡️ [MODO ASISTIDO] Abriendo navegador para [{platform.upper()}].")
        self._log("👉 Resuelve el reto de Cloudflare ('Verifica que eres humano') o 2FA en la ventana de Chrome.")
        self.assisted_button.configure(state="disabled", text="⏳ ASISTIDO ACTIVO...")

        def worker():
            try:
                from src.automation.manual_login_booster import run_assisted_login
                import asyncio
                asyncio.run(run_assisted_login(platform))
                self._log(f"✨ Modo asistido finalizado para [{platform.upper()}]. Las cookies y sesión quedaron guardadas.")
            except Exception as e:
                self._log(f"Nota en modo asistido: {e}")
            finally:
                self.after(0, lambda: self.assisted_button.configure(state="normal", text="🛡️ MODO ASISTIDO (CLOUDFLARE / 2FA)"))

        threading.Thread(target=worker, daemon=True).start()

def main():
    app = VelvetControlCenter()
    app.mainloop()

if __name__ == "__main__":
    main()
