import type { APIRoute } from 'astro';
import { candidates, pillars } from '../lib/data';
import { SITE_CONFIG } from '../lib/config';

export const GET: APIRoute = () => {
  const siteUrl = SITE_CONFIG.url;
  const currentDate = new Date().toISOString();
  
  // Páginas estáticas principales
  const staticPages = [
    { url: '', priority: '1.0', changefreq: 'daily' },
    { url: 'metodologia', priority: '0.9', changefreq: 'weekly' },
    { url: 'ranking', priority: '0.9', changefreq: 'daily' },
    { url: 'comparar', priority: '0.8', changefreq: 'weekly' },
    { url: 'candidatos', priority: '0.8', changefreq: 'daily' },
    { url: 'pilares', priority: '0.8', changefreq: 'weekly' },
    { url: 'acerca', priority: '0.6', changefreq: 'monthly' },
    { url: 'tecnico', priority: '0.5', changefreq: 'monthly' },
  ];
  
  // Páginas dinámicas de candidatos
  const candidatePages = candidates.map(c => ({
    url: `candidatos/${c.candidate_id}`,
    priority: '0.7',
    changefreq: 'weekly'
  }));
  
  // Páginas dinámicas de pilares
  const pillarPages = pillars.map(p => ({
    url: `pilares/${p.pillar_id}`,
    priority: '0.7',
    changefreq: 'weekly'
  }));
  
  const allPages = [...staticPages, ...candidatePages, ...pillarPages];
  
  const sitemap = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${allPages.map(page => `  <url>
    <loc>${siteUrl}/${page.url}</loc>
    <lastmod>${currentDate}</lastmod>
    <changefreq>${page.changefreq}</changefreq>
    <priority>${page.priority}</priority>
  </url>`).join('\n')}
</urlset>`;
  
  return new Response(sitemap, {
    headers: {
      'Content-Type': 'application/xml; charset=utf-8',
      'Cache-Control': 'public, max-age=3600'
    }
  });
};
