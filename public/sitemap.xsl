<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="2.0" 
                xmlns:html="http://www.w3.org/TR/REC-html40"
                xmlns:sitemap="http://www.sitemaps.org/schemas/sitemap/0.9"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output method="html" version="1.0" encoding="UTF-8" indent="yes"/>
  <xsl:template match="/">
    <html xmlns="http://www.w3.org/1999/xhtml" lang="en">
      <head>
        <title>XML Sitemap | UniqueDigit</title>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <style type="text/css">
          * { box-sizing: border-box; margin: 0; padding: 0; }
          body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background-color: #f8fafc;
            color: #1e293b;
            padding: 2rem 1rem;
            line-height: 1.5;
          }
          .container {
            max-width: 1100px;
            margin: 0 auto;
            background: #ffffff;
            border-radius: 16px;
            border: 1px solid #e2e8f0;
            box-shadow: 0 4px 20px -2px rgba(15, 23, 42, 0.05);
            overflow: hidden;
          }
          .header {
            background: linear-gradient(135deg, #5B2FD0 0%, #3E1FA0 100%);
            color: #ffffff;
            padding: 2rem;
          }
          .header h1 {
            font-size: 1.75rem;
            font-weight: 800;
            margin-bottom: 0.5rem;
            letter-spacing: -0.02em;
          }
          .header p {
            color: #e9d5ff;
            font-size: 0.95rem;
            max-width: 700px;
          }
          .stats {
            padding: 1.25rem 2rem;
            background: #f1f5f9;
            border-bottom: 1px solid #e2e8f0;
            display: flex;
            align-items: center;
            justify-content: space-between;
            font-size: 0.875rem;
            font-weight: 600;
            color: #475569;
          }
          .badge {
            background: #5B2FD0;
            color: #ffffff;
            padding: 0.25rem 0.75rem;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 700;
          }
          table {
            width: 100%;
            border-collapse: collapse;
            text-align: left;
            font-size: 0.875rem;
          }
          th {
            background-color: #f8fafc;
            color: #64748b;
            font-weight: 700;
            text-transform: uppercase;
            font-size: 0.75rem;
            letter-spacing: 0.05em;
            padding: 0.875rem 1.5rem;
            border-bottom: 1px solid #e2e8f0;
          }
          td {
            padding: 0.875rem 1.5rem;
            border-bottom: 1px solid #f1f5f9;
          }
          tr:hover td {
            background-color: #f8faff;
          }
          a {
            color: #5B2FD0;
            text-decoration: none;
            font-weight: 500;
            word-break: break-all;
          }
          a:hover {
            text-decoration: underline;
          }
          .pill {
            display: inline-block;
            padding: 0.15rem 0.5rem;
            border-radius: 6px;
            font-size: 0.75rem;
            font-weight: 600;
            background: #e2e8f0;
            color: #334155;
          }
          .footer {
            padding: 1.5rem 2rem;
            text-align: center;
            font-size: 0.8125rem;
            color: #94a3b8;
            border-top: 1px solid #e2e8f0;
          }
        </style>
      </head>
      <body>
        <div class="container">
          <div class="header">
            <h1>UniqueDigit XML Sitemap</h1>
            <p>This is a machine-readable XML sitemap generated for search engines like Google and Bing. Below is a human-friendly visual representation of all indexable URLs.</p>
          </div>
          <div class="stats">
            <div>
              Total Indexable URLs: <xsl:value-of select="count(sitemap:urlset/sitemap:url)"/>
            </div>
            <div class="badge">Google Search Console Ready</div>
          </div>
          <table>
            <thead>
              <tr>
                <th style="width: 55%;">URL Location</th>
                <th style="width: 15%;">Priority</th>
                <th style="width: 15%;">Change Frequency</th>
                <th style="width: 15%;">Last Modified</th>
              </tr>
            </thead>
            <tbody>
              <xsl:for-each select="sitemap:urlset/sitemap:url">
                <tr>
                  <td>
                    <a href="{sitemap:loc}" target="_blank">
                      <xsl:value-of select="sitemap:loc"/>
                    </a>
                  </td>
                  <td>
                    <span class="pill">
                      <xsl:value-of select="sitemap:priority"/>
                    </span>
                  </td>
                  <td>
                    <span class="pill">
                      <xsl:value-of select="sitemap:changefreq"/>
                    </span>
                  </td>
                  <td style="color: #64748b; font-family: monospace;">
                    <xsl:value-of select="sitemap:lastmod"/>
                  </td>
                </tr>
              </xsl:for-each>
            </tbody>
          </table>
          <div class="footer">
            Generated autonomously by UniqueDigit Editorial Engine • Updated continuously
          </div>
        </div>
      </body>
    </html>
  </xsl:template>
</xsl:stylesheet>
