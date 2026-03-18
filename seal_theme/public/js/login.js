(function () {
  function chooseMode(img) {
    if (!img || !img.parentElement) return;

    // Get container size
    var rect = img.parentElement.getBoundingClientRect();

    // If the image is larger than its box in either dimension, use cover (crop to fill).
    // Otherwise show at natural size.
    var cover = (img.naturalWidth > rect.width) || (img.naturalHeight > rect.height);

    // Switch classes only if needed (prevents unnecessary repaints)
    img.classList.toggle('mode-cover', cover);
    img.classList.toggle('mode-natural', !cover);

    // Reveal if not already visible
    if (!img.classList.contains('is-ready')) {
      // Using rAF ensures we apply mode before revealing (no flash)
      requestAnimationFrame(function () {
        img.classList.add('is-ready');
      });
    }
  }

  function fitAll(scope) {
    (scope || document).querySelectorAll('.login-left .app-logo').forEach(function (img) {
      if (img.complete && img.naturalWidth) {
        chooseMode(img);
      } else {
        img.addEventListener('load', function onLoad() {
          img.removeEventListener('load', onLoad);
          chooseMode(img);
        });
      }

      // Re-fit if the container resizes
      if (window.ResizeObserver) {
        var ro = new ResizeObserver(function () { chooseMode(img); });
        ro.observe(img.parentElement);
      }
    });
  }

  // Run on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () { fitAll(document); });
  } else {
    fitAll(document);
  }

  // Fallback: also re-check on window resize (debounced)
  var t;
  window.addEventListener('resize', function () {
    clearTimeout(t);
    t = setTimeout(function () { fitAll(document); }, 120);
  });
})();