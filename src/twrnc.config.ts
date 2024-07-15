// twrnc.config.js
const { create } = require("twrnc");

const customConfig = {
  theme: {
    darkMode: "class",
    extend: {
      colors: {
        light: {
          primary: "#215273",
          secondary: "#55C597",
          base: "#fffff",
          content: "#ffffff",
        },
        dark: {
          primary: "#215273",
          secondary: "#55C597",
          base: "#000000",
          content: "#ffffff",
        },
      },
    },
  },
};

module.exports = create(customConfig);
