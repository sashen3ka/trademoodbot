/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
theme: {
  extend: {
    colors: {
      dark: "#10151F",
      light: "#F2F2F2",
      grayish: "#9BA5B2",
      accent: "#00F7C3",
    },
  },
},

  plugins: [],
};