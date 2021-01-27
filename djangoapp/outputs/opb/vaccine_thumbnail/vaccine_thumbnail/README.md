Layer Cake Example
===

This is a starter example for using [Layer Cake](https://layercake.graphics).

*Note that you will need to have [Node.js](https://nodejs.org) installed.*

## Get started

Install the dependencies...

```bash
npm install
npm run build && npm start
```

Your app will be running at [localhost:5000](http://localhost:5000).

## Developing

```sh
# if you didn't already install, run the install command
npm install
npm run dev
```

Your app will be running at [localhost:5000](http://localhost:5000).

## Server-side rendering

This template also lets you pre-render your project, which will build out the elements that don't rely on any client-side JavaScript.

```sh
npm run build:ssr
npm start
```

Your app will be running at [localhost:5000](http://localhost:5000).

#### Hydrating

Sometimes you want to build out the HTML but your graphic still relies on some client-side JavaScript. In these cases, set `hydrate: true` in the `config.json` file. That will set the `hydratable` [compiler option](https://svelte.dev/docs#svelte_compile) and the `hydrate` [runtime option](https://svelte.dev/docs#Creating_a_component) to `true`. It will also add a script tag to load the `build/bundle.js` JavaScript file.

## Additional info

This is a fairly basic setup that has just enough to get you going with LayerCake and SSR rendering. For a more complete Svelte setup, take a look at Russell Goldenberg's [svelte-starter](https://github.com/russellgoldenberg/svelte-starter).
