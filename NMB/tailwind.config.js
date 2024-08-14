/** @type {import('tailwindcss').Config} */
module.exports = {
    content: ["./dist/**/*.{html,js}"],
    theme: {
      fontFamily: {
        'sans': ['Padauk', 'sans-serif'],
        'serif': ['Noto Serif Myanmar', 'serif'],
      },
      extend: {
        lineHeight: {
          'extra-loose': '2.5',
        }},
    },
    plugins: [
      require('@tailwindcss/typography')
    ],
  }