/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{html,js}"],
  theme: {
    extend: {
      height: {
        //'62': '15.5rem',
        '62': '80rem',
      },
      borderWidth: {
        DEFAULT: '1px',
        '0': '0',
        '1': '1px',
      },
      fontWeight: {
        mediumbold: 600,
      },
    },
  },
  plugins: [],
}