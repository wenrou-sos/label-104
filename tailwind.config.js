/** @type {import('tailwindcss').Config} */

export default {
  darkMode: "class",
  content: ["./index.html", "./src/**/*.{js,ts,vue}"],
  theme: {
    container: {
      center: true,
    },
    extend: {
      colors: {
        primary: {
          50: '#FDF2F8',
          100: '#FCE7F3',
          200: '#FBCFE8',
          300: '#F9A8D4',
          400: '#F472B6',
          500: '#E8A0BF',
          600: '#DB7093',
          700: '#BE185D',
          800: '#9D174D',
          900: '#831843',
        },
        secondary: {
          50: '#F5F3FF',
          100: '#EDE9FE',
          200: '#DDD6FE',
          300: '#C4B5FD',
          400: '#A78BFA',
          500: '#6B5B95',
          600: '#5B4B8A',
          700: '#4C1D95',
          800: '#4C1D95',
          900: '#3B0764',
        },
        cream: {
          50: '#FFFCFA',
          100: '#FFF9F5',
          200: '#FFF0E6',
          300: '#FFE4D1',
          400: '#FFD4B8',
          500: '#F5C6A5',
        },
      },
      borderRadius: {
        '12': '12px',
        'card': '12px',
      },
      boxShadow: {
        'card': '0 2px 12px rgba(0, 0, 0, 0.06)',
        'card-hover': '0 4px 20px rgba(0, 0, 0, 0.1)',
      },
    },
  },
  plugins: [],
};
