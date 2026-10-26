// ==============================================================================
// SIREN AI — Service Worker Oficial (PWA, Cache Shell & Web Push en Tiempo Real)
// ==============================================================================
const CACHE_NAME = 'siren-ai-v1.0.8';
const SHELL_ASSETS = [
  './',
  './index.html',
  './manifest.json',
  './icons/icon-192x192.png',
  './icons/icon-512x512.png',
  './icons/icon-512x512-maskable.png',
  './icons/badge-72x72.png',
  './icons/assistant-roxanne.png',
  './icons/assistant-chloe.png',
  './icons/assistant-diana.png',
  './icons/assistant-electra.png'
];

// 1. INSTALACIÓN: Pre-cachear el App Shell
self.addEventListener('install', event => {
  self.skipWaiting();
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      return cache.addAll(SHELL_ASSETS).catch(err => {
        console.warn('[SW] Cache precache partial:', err);
      });
    })
  );
});

// 2. ACTIVACIÓN: Limpiar cachés antiguas y tomar control de clientes
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys => {
      return Promise.all(
        keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k))
      );
    }).then(() => self.clients.claim())
  );
});

// 3. FETCH: Network-first con fallback a caché (no interferir con llamadas /api)
self.addEventListener('fetch', event => {
  const url = new URL(event.request.url);

  // Ignorar peticiones API dinámicas, túneles o websocket para evitar respuestas obsoletas
  if (url.pathname.startsWith('/api/') || event.request.method !== 'GET') {
    return;
  }

  event.respondWith(
    fetch(event.request)
      .then(networkResponse => {
        // Almacenar copia en caché si es válida
        if (networkResponse && networkResponse.status === 200) {
          const resClone = networkResponse.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(event.request, resClone));
        }
        return networkResponse;
      })
      .catch(() => caches.match(event.request))
  );
});

// 4. PUSH NOTIFICATION: Recepción de Notificaciones Web Push del Servidor SIREN
self.addEventListener('push', event => {
  console.log('[SW] Push Event recibido');

  let payload = {
    title: 'SIREN AI - Sam Barton',
    body: 'Tienes un nuevo mensaje de tu asistente',
    assistant: 'roxanne',
    tag: 'siren-general',
    url: '/?tab=tab-asistentes&assistant=roxanne',
    timestamp: Date.now()
  };

  if (event.data) {
    try {
      const parsed = event.data.json();
      payload = Object.assign(payload, parsed);
    } catch (e) {
      payload.body = event.data.text();
    }
  }

  // Iconos personalizados de cada asistente
  const assistantIcons = {
    'roxanne': './icons/assistant-roxanne.png',
    'chloe': './icons/assistant-chloe.png',
    'diana': './icons/assistant-diana.png',
    'electra': './icons/assistant-electra.png'
  };

  const notificationIcon = assistantIcons[payload.assistant] || './icons/icon-192x192.png';
  const notificationBadge = './icons/badge-72x72.png';

  // Configuración completa para Pantalla de Bloqueo Android, Sonido y Vibración
  const notificationOptions = {
    body: payload.body,
    icon: notificationIcon,
    badge: notificationBadge,
    tag: payload.tag || `siren-${payload.assistant}`, // Control estricto de duplicados
    renotify: true, // Si hay nuevo mensaje con el mismo tag, vuelve a sonar y vibrar
    requireInteraction: true, // Mantiene la notificación visible en la pantalla de bloqueo
    vibrate: [250, 100, 250, 100, 250], // Patrón de vibración táctil
    silent: false,
    timestamp: payload.timestamp || Date.now(),
    data: {
      url: payload.url || `./?tab=tab-asistentes&assistant=${payload.assistant || 'roxanne'}`,
      assistant: payload.assistant || 'roxanne'
    },
    actions: [
      { action: 'open_chat', title: '💬 Abrir Chat' },
      { action: 'dismiss', title: 'Descartar' }
    ]
  };

  event.waitUntil(
    self.registration.showNotification(payload.title, notificationOptions)
  );
});

// 5. CLIC EN NOTIFICACIÓN: Abrir la PWA y Enfocar el Asistente Correcto
self.addEventListener('notificationclick', event => {
  event.notification.close();

  if (event.action === 'dismiss') {
    return;
  }

  const notificationData = event.notification.data || {};
  const targetAssistant = notificationData.assistant || 'roxanne';
  const targetUrl = notificationData.url || `./?tab=tab-asistentes&assistant=${targetAssistant}`;

  event.waitUntil(
    clients.matchAll({ type: 'window', includeUncontrolled: true }).then(windowClients => {
      // 1. Si ya hay una ventana o pestaña abierta de SIREN AI, enfocarla y enviarle mensaje
      for (const client of windowClients) {
        if ('focus' in client) {
          client.focus();
          client.postMessage({
            type: 'NAVIGATE_ASSISTANT',
            tab: 'tab-asistentes',
            assistant: targetAssistant
          });
          return;
        }
      }
      // 2. Si la app estaba cerrada, abrir una nueva ventana con la URL directa
      if (clients.openWindow) {
        return clients.openWindow(targetUrl);
      }
    })
  );
});
