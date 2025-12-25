/** @type {import('tailwindcss').Config} */
export default {
    darkMode: 'selector',
    content: [
        "./src/**/*.{js,ts,jsx,tsx,mdx}",
    ],
    theme: {
        extend: {
            fontFamily: {
                sans: ['var(--font-roboto)', 'Roboto', 'ui-sans-serif', 'system-ui', 'sans-serif'],
                body: ['var(--font-roboto)', 'Roboto', 'ui-sans-serif', 'system-ui', 'sans-serif'],
            },
        },
    },
    plugins: [],
}
