/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        brand: {
          DEFAULT: '#5B2FD0',
          dark: '#3E1FA0',
          soft: '#EFEAFD',
        },
        ink: {
          DEFAULT: '#111827',
          dark: '#F3F2FA',
        },
        muted: {
          DEFAULT: '#6B7280',
          dark: '#A4A0BC',
        },
        bg: {
          DEFAULT: '#F6F5FB',
          dark: '#0F0D1A',
        },
        card: {
          DEFAULT: '#FFFFFF',
          dark: '#181528',
        },
        line: {
          DEFAULT: '#E8E6F0',
          dark: '#2A2644',
        },
        breaking: '#E11D2E',
        cta: {
          DEFAULT: '#FFD21F',
          ink: '#1A1A1A',
        },
        tech: {
          DEFAULT: '#2F80ED',
          bg: '#DCEFFB',
        },
        money: {
          DEFAULT: '#D99A00',
          bg: '#FFF1CC',
        },
        life: {
          DEFAULT: '#1FA971',
          bg: '#DDF5E7',
        },
        ent: {
          DEFAULT: '#E0348B',
          bg: '#FDE1EE',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
      },
      borderRadius: {
        '2xl': '16px',
        'xl': '12px',
        'lg': '10px',
      },
      boxShadow: {
        soft: '0 8px 30px rgba(40, 20, 100, 0.08)',
        card: '0 4px 20px rgba(0, 0, 0, 0.04)',
      }
    },
  },
  plugins: [],
};
