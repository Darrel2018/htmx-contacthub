/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./contacts/templates/**/*.html",
    "./contacts/static/**/*.js",
  ],
  theme: {
    extend: {},
  },
  plugins: [require("daisyui")],
};
