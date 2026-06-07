/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        "inverse-surface": "#d4e4fa",
        "tertiary-fixed": "#ffdad7",
        "secondary-fixed-dim": "#4edea3",
        "background": "#051424",
        "inverse-primary": "#005ac2",
        "outline": "#8c909f",
        "outline-variant": "#424754",
        "on-surface": "#d4e4fa",
        "surface-dim": "#051424",
        "primary-fixed-dim": "#adc6ff",
        "on-secondary-fixed": "#002113",
        "surface-container-highest": "#273647",
        "surface-tint": "#adc6ff",
        "surface-variant": "#273647",
        "on-tertiary": "#68000a",
        "surface-bright": "#2c3a4c",
        "on-secondary-fixed-variant": "#005236",
        "on-surface-variant": "#c2c6d6",
        "on-primary": "#002e6a",
        "primary-container": "#4d8eff",
        "on-secondary-container": "#00311f",
        "tertiary-fixed-dim": "#ffb3ad",
        "secondary-fixed": "#6ffbbe",
        "on-primary-fixed-variant": "#004395",
        "on-tertiary-fixed": "#410004",
        "surface-container-low": "#0d1c2d",
        "surface-container-high": "#1c2b3c",
        "surface": "#051424",
        "on-primary-fixed": "#001a42",
        "error": "#ffb4ab",
        "tertiary": "#ffb3ad",
        "primary-fixed": "#d8e2ff",
        "on-background": "#d4e4fa",
        "error-container": "#93000a",
        "on-error": "#690005",
        "secondary": "#4edea3",
        "on-tertiary-fixed-variant": "#930013",
        "on-primary-container": "#00285d",
        "surface-container-lowest": "#010f1f",
        "tertiary-container": "#ff5451",
        "surface-container": "#122131",
        "inverse-on-surface": "#233143",
        "on-tertiary-container": "#5c0008",
        "on-secondary": "#003824",
        "secondary-container": "#00a572",
        "on-error-container": "#ffdad6",
        "primary": "#adc6ff"
      },
      borderRadius: {
        "DEFAULT": "0.25rem",
        "lg": "0.5rem",
        "xl": "0.75rem",
        "full": "9999px"
      },
      spacing: {
        "base": "4px",
        "gutter": "16px",
        "xl": "32px",
        "sm": "8px",
        "xs": "4px",
        "md": "16px",
        "margin": "24px",
        "lg": "24px"
      },
      fontFamily: {
        "display-lg": ["Inter", "sans-serif"],
        "mono-data": ["Geist", "monospace"],
        "headline-lg-mobile": ["Inter", "sans-serif"],
        "headline-md": ["Inter", "sans-serif"],
        "body-lg": ["Inter", "sans-serif"],
        "headline-lg": ["Inter", "sans-serif"],
        "body-md": ["Inter", "sans-serif"],
        "label-md": ["Geist", "monospace"]
      },
      fontSize: {
        "display-lg": ["48px", {"lineHeight": "56px", "letterSpacing": "-0.02em", "fontWeight": "700"}],
        "mono-data": ["13px", {"lineHeight": "18px", "fontWeight": "400"}],
        "headline-lg-mobile": ["24px", {"lineHeight": "32px", "fontWeight": "600"}],
        "headline-md": ["20px", {"lineHeight": "28px", "fontWeight": "600"}],
        "body-lg": ["16px", {"lineHeight": "24px", "fontWeight": "400"}],
        "headline-lg": ["32px", {"lineHeight": "40px", "letterSpacing": "-0.01em", "fontWeight": "600"}],
        "body-md": ["14px", {"lineHeight": "20px", "fontWeight": "400"}],
        "label-md": ["12px", {"lineHeight": "16px", "letterSpacing": "0.02em", "fontWeight": "500"}]
      },
      keyframes: {
        "slide-in-right": {
            "0%": { transform: "translateX(100%)", opacity: "0" },
            "100%": { transform: "translateX(0)", opacity: "1" }
        },
        "slide-in-up": {
            "0%": { transform: "translateY(20px)", opacity: "0" },
            "100%": { transform: "translateY(0)", opacity: "1" }
        },
        "pulse-text": {
            "0%, 100%": { opacity: "1" },
            "50%": { opacity: "0.75" }
        },
        "fadeUp": {
            "0%": { opacity: "0", transform: "translateY(20px)" },
            "100%": { opacity: "1", transform: "translateY(0)" }
        },
        "ticker": {
            "0%": { transform: "translateX(100%)" },
            "100%": { transform: "translateX(-100%)" }
        }
      },
      animation: {
        "slide-in-right": "slide-in-right 0.4s ease-out forwards",
        "slide-in-up": "slide-in-up 0.5s ease-out forwards",
        "pulse-text": "pulse-text 2.5s ease-in-out infinite",
        "fade-up": "fadeUp 0.8s ease-out forwards",
        "ticker": "ticker 120s linear infinite"
      }
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
  ],
}
