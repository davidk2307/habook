/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{html,js}"],
  theme: {
    colors:
    {
      'oxford_blue': {
        DEFAULT: '#102542',
        100: '#03070d',
        200: '#060f1a',
        300: '#0a1627',
        400: '#0d1d35',
        500: '#102542',
        600: '#214b87',
        700: '#3172cc',
        800: '#75a1de',
        900: '#bad0ee'
      }, 'bittersweet': {
        DEFAULT: '#f87060',
        100: '#420903',
        200: '#831205',
        300: '#c51b08',
        400: '#f6321c',
        500: '#f87060',
        600: '#fa8a7e',
        700: '#fba79e',
        800: '#fcc5be',
        900: '#fee2df'
      }, 'platinum': {
        DEFAULT: '#cdd7d6',
        100: '#252e2e',
        200: '#4a5d5b',
        300: '#708b89',
        400: '#9eb1af',
        500: '#cdd7d6',
        600: '#d6dede',
        700: '#e0e6e6',
        800: '#ebefee',
        900: '#f5f7f7'
      }, 'khaki': {
        DEFAULT: '#b3a394',
        100: '#26201b',
        200: '#4c4136',
        300: '#736151',
        400: '#98826d',
        500: '#b3a394',
        600: '#c2b5a9',
        700: '#d1c8bf',
        800: '#e1dad4',
        900: '#f0edea'
      }, 'white': {
        DEFAULT: '#ffffff',
        100: '#333333',
        200: '#666666',
        300: '#999999',
        400: '#cccccc',
        500: '#ffffff',
        600: '#ffffff',
        700: '#ffffff',
        800: '#ffffff',
        900: '#ffffff'
      }
    },
    extend: {},
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography')
  ],
}

