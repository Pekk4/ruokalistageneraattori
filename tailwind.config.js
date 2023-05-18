/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{html,js}"],
  theme: {
    extend: {
      height: {
        //'62': '15.5rem',
        '62': '80rem',
        '100': '650px',
      },
      borderWidth: {
        DEFAULT: '1px',
        '0': '0',
        '1': '1px',
      },
      fontWeight: {
        mediumbold: 600,
      },
      textShadow: {
        'sm-black': '1px 1px 2px rgb(0 0 0);',
        'sm-emerald': '1px 1px 2px rgb(22 163 74);',
        '2md': '2px 2px 3px rgb(255 255 255 / 95%);',
        '3md': '3px 3px 4px rgb(255 255 255);',
        '3xl': '0px 1px 2px rgba(0, 0, 0, 0.5), 1px 2px 4px rgb(0, 0, 0)',
        '4xl': '1px 2px 3px rgba(255, 255, 255, 0.5), 2px 4px 6px rgb(255, 255, 255)',
      },
    },
  },
  plugins: [require('tailwindcss-textshadow')],
}