/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      colors: {
        'modu-mint': '#BCEBD4',
        'modu-arctic': '#F5F9F7',
        'modu-dark': '#1A1C1E',
      },
      backgroundImage: {
        'modu-home': "url('/assets/ModuHome Background JAN.png')",
      }
    },
  },
  plugins: [],
};
