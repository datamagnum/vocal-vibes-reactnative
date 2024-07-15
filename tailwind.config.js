/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx}"],
  presets: [require("nativewind/preset")],
  theme: {
    darkMode: 'class',
    extend: {
      colors: {
        light: {
          primary: "#215273",
          secondary: "#55C597",
          base: "#ffffff",
          content: "#ffffff",
        },
        dark: {
          primary: "#215273",
          secondary: "#55C597",
          base: "#000000",
          content: "#ffffff",
        }
      },
    },
  },
  plugins: [],
}

