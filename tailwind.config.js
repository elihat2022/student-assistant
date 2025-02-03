/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./dashboard/templates/**/*.html",
    "./account/templates/**/*.html",
    "./templates/**/*.html",
    "./static/**/*.js",
    "./static/**/*.css",
  ],
  theme: {
    extend: {
      fontFamily: {
        'Open-Sans': ['Open Sans']
      }
    },
  },
  

}