/**
 * SIREN AI — Paleta de Colores Centralizada
 * 
 * Paleta extraída de la identidad visual oficial (Sci-Fi / Bioma Cósmico):
 * - HEX #8B53FF (RGB 139, 83, 255)  -> Primary (Púrpura Neón Eléctrico)
 * - HEX #1E2432 (RGB 30, 36, 50)    -> Primary Dark (Azul Noche Profundo / Base)
 * - HEX #1AE589 (RGB 26, 229, 139)  -> Accent Green (Verde Neón Bio-luminiscente / Éxito)
 * - HEX #F2F2F2 (RGB 242, 242, 242) -> Light Surface (Blanco Suave / Modo Claro)
 */

export const SIREN_AI = {
  /** Púrpura Eléctrico Neón — Color de marca, botones principales y avatar */
  primary: '#8B53FF',
  primaryRgb: '139, 83, 255',

  /** Púrpura suave para estados hover y degradados */
  primaryLight: '#A77BFF',

  /** Azul Noche Profundo — Fondo oscuro, texto en modo claro y acentos estructurados */
  primaryDark: '#1E2432',
  primaryDarkRgb: '30, 36, 50',

  /** Superficies y tarjetas en modo oscuro (variantes armónicas de primaryDark) */
  darkSurface: '#181D29',
  darkCard: '#262D3D',
  darkCardHover: '#2E364A',
  darkBorder: 'rgba(242, 242, 242, 0.08)',

  /** Verde Neón Esmeralda — Acentos bio-tecnológicos, estados activos, badges y éxito */
  accentGreen: '#1AE589',
  accentGreenRgb: '26, 229, 139',
  accentGreenHover: '#17CF7B',

  /** Blanco Suave / Claro — Fondo general en Modo Claro y texto en Modo Oscuro */
  lightBackground: '#F2F2F2',
  lightBackgroundRgb: '242, 242, 242',

  /** Superficies en modo claro */
  lightSurface: '#FFFFFF',
  lightCardHover: '#EBEBEB',
  lightBorder: 'rgba(30, 36, 50, 0.08)',
  lightTextMuted: '#525B6F',
  lightTextDim: '#737E94',

  /** Semánticos y Estados — Derivados estrictamente de la paleta oficial (HEX 8B53FF, 1E2432, 1AE589, F2F2F2) */
  success: '#1AE589',
  warning: '#8B53FF',
  danger: '#8B53FF',
  info: '#1AE589',

  /** Sombras y Resplandores Glow */
  glowPurple: '0 0 25px rgba(139, 83, 255, 0.25)',
  glowGreen: '0 0 25px rgba(26, 229, 139, 0.25)',
  shadowCard: '0 8px 32px rgba(30, 36, 50, 0.35)',
} as const;

export type SirenTheme = typeof SIREN_AI;

/** Helper para inyectar las variables CSS nativas en el DOM */
export function getSirenCssVariables(): string {
  return `
    :root {
      --primary: ${SIREN_AI.primary};
      --primary-light: ${SIREN_AI.primaryLight};
      --primary-dark: ${SIREN_AI.primaryDark};
      --secondary: ${SIREN_AI.accentGreen};
      --accent-green: ${SIREN_AI.accentGreen};
      --success: ${SIREN_AI.success};
      --bg-dark: ${SIREN_AI.primaryDark};
      --bg-surface: ${SIREN_AI.darkSurface};
      --bg-card: ${SIREN_AI.darkCard};
      --bg-card-hover: ${SIREN_AI.darkCardHover};
      --text-main: ${SIREN_AI.lightBackground};
    }
    body.light-theme {
      --bg-dark: ${SIREN_AI.lightBackground};
      --bg-surface: ${SIREN_AI.lightSurface};
      --bg-card: ${SIREN_AI.lightSurface};
      --text-main: ${SIREN_AI.primaryDark};
      --border-color: ${SIREN_AI.lightBorder};
    }
  `;
}

export default SIREN_AI;
