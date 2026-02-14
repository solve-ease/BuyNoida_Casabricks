/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        page: 'rgb(var(--color-page) / <alpha-value>)',
        brand: 'rgb(var(--color-brand) / <alpha-value>)',
        'brand-dark': 'rgb(var(--color-brand-dark) / <alpha-value>)',
        'brand-ink': 'rgb(var(--color-brand-ink) / <alpha-value>)',
        'wave-light': 'rgb(var(--color-wave-light) / <alpha-value>)',
      },
      backgroundImage: {
        'hero-gradient': 'linear-gradient(180deg, #f4f6fa 0%, #eef2f7 54%, #e7edf6 100%)',
      },
    },
  },
  plugins: [],
}
