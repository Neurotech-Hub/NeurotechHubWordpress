# NeurotechHubWordpress

Custom CSS for https://neurotechhub.wustl.edu/, hosted on GitHub and loaded from the site footer.

## Usage

Raw GitHub URLs (`raw.githubusercontent.com`) are served as `text/plain` with `nosniff`, so browsers refuse to apply them as stylesheets. Load the file through jsDelivr instead:

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/<user>/NeurotechHubWordpress@main/neurotechhub.css">
```

If `<link>` tags are stripped by WordPress, use `@import` inside a `<style>` tag:

```html
<style>
@import url("https://cdn.jsdelivr.net/gh/<user>/NeurotechHubWordpress@main/neurotechhub.css");
</style>
```

jsDelivr caches branch URLs for up to 12 hours. To see changes immediately, either pin a commit/tag (`@<sha>` or `@v1`) or purge the cache at `https://purge.jsdelivr.net/gh/<user>/NeurotechHubWordpress@main/neurotechhub.css`.
