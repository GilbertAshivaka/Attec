# ATTEC Website - Frontend

Beautiful, modern website for ATTEC (Advancing Technology for Tomorrow's Engineering and Computing) - an AI consulting and development company based in Kenya.

## Features

- ✨ Modern, clean design inspired by SpaceX, Apple, and Figure
- 🎨 Smooth animations with Framer Motion
- 📱 Fully responsive (mobile, tablet, desktop)
- ⚡ Fast performance with Vite
- 🎯 SEO optimized
- 🔄 Intersection Observer for scroll animations
- 💼 Professional service showcases
- 📝 Contact form with validation

## Tech Stack

- **React** - UI framework
- **Vite** - Build tool
- **Framer Motion** - Animations
- **React Intersection Observer** - Scroll-based animations
- **Lucide React** - Icons
- **CSS3** - Styling

## Getting Started

### Prerequisites

- Node.js 20.19+ or 22.12+
- pnpm

### Installation

```bash
# Install dependencies
pnpm install

# Start development server
pnpm dev

# Build for production
pnpm build

# Preview production build
pnpm preview
```

## Project Structure

```
frontend/
├── public/
│   └── logo.jpg          # ATTEC logo
├── src/
│   ├── components/       # React components
│   │   ├── Navigation.jsx
│   │   ├── Hero.jsx
│   │   ├── Story.jsx
│   │   ├── Services.jsx
│   │   ├── Process.jsx
│   │   ├── About.jsx
│   │   └── Contact.jsx
│   ├── App.jsx           # Main app component
│   ├── App.css           # App styles
│   ├── index.css         # Global styles
│   └── main.jsx          # Entry point
└── index.html            # HTML template
```

## Sections

1. **Hero** - Eye-catching introduction with logo and call-to-action
2. **Story** - Company narrative and value proposition
3. **Services** - Three-tier service offerings with pricing
4. **Process** - Four-step workflow visualization
5. **About** - Company mission, values, and location
6. **Contact** - Contact form and company information

## Customization

### Colors

The website uses a monochromatic palette based on grays and blacks. To customize:

- Primary: `#111827` (Dark gray/black)
- Secondary: `#374151` (Medium gray)
- Text: `#4b5563` and `#6b7280` (Light grays)
- Background: `#ffffff` and `#f9fafb`
- Accent: `#10b981` (Green for success states)

### Typography

- Font family: Inter (loaded from Google Fonts)
- Headings: Bold (700-900 weight)
- Body: Regular (400 weight)

## Performance

- Optimized images
- Lazy loading with Intersection Observer
- Minimal bundle size
- Fast Time to Interactive (TTI)

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Future Enhancements

- [ ] Add blog/insights section
- [ ] Implement case studies page
- [ ] Add testimonials carousel
- [ ] Integrate with backend API for contact form
- [ ] Add calendar booking integration
- [ ] Multi-language support

## License

Copyright © 2025 ATTEC. All rights reserved.

## React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project.
