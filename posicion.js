const puppeteer = require('puppeteer');

async function obtenerHrefsPaginas(paginas) {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  
  const hrefs = [];

  // Función para simular scroll para cargar más elementos
  async function autoScroll() {
    await page.evaluate(async () => {
      await new Promise((resolve, reject) => {
        let lastHeight = 0;

        const timer = setInterval(() => {
          const scrollHeight = document.documentElement.scrollHeight;
          window.scrollBy(0, window.innerHeight);
          const newHeight = document.documentElement.scrollHeight;

          if (newHeight === lastHeight) {
            clearInterval(timer);
            resolve();
          }

          lastHeight = newHeight;
        }, 100);
      });
    });
  }

  for (let i = 1; i <= paginas; i++) {
    const url = `https://streamate.com/page/${i}`;
    await page.goto(url, { waitUntil: 'load' });

    await autoScroll();

    const nuevosHrefs = await page.evaluate(() => {
      const streamerNodes = document.querySelectorAll('[data-ta-locator="PerformerList"] > div > div > div > div > div > div');
      const hrefs = Array.from(streamerNodes).map(node => {
        const aElement = node.querySelector('a');
        return aElement ? aElement.getAttribute('href') : null;
      });
      return hrefs.filter(href => href !== null);
    });

    hrefs.push(...nuevosHrefs);
  }

  await browser.close();

  return hrefs;
}

// Ejecutar la función para obtener los hrefs de las páginas 1 y 2
obtenerHrefsPaginas(2)
  .then(hrefs => {
    console.log('Todos los hrefs de las páginas 1 y 2:', hrefs);
  })
  .catch(error => {
    console.error('Error al obtener los hrefs de las páginas 1 y 2:', error);
  });
