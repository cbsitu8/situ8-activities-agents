/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{html,js,svelte,ts}'],
  theme: {
    extend: {
      colors: {
        'sop-primary': '#2563eb',
        'sop-secondary': '#64748b',
        'sop-success': '#059669',
        'sop-warning': '#d97706',
        'sop-error': '#dc2626',
        'sop-critical': '#991b1b'
      }
    },
  },
  plugins: [
    require('@tailwindcss/forms')
  ],
}