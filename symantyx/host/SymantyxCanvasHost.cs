using System;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using Microsoft.Web.WebView2.Core;
using Microsoft.Web.WebView2.Wpf;

namespace SymantyxCanvasHost
{
    public partial class MainWindow : Window
    {
        private readonly HttpClient _http = new HttpClient();
        public MainWindow()
        {
            InitializeComponent();
            InitializeAsync();
        }

        private async void InitializeAsync()
        {
            var env = await CoreWebView2Environment.CreateAsync();
            await webView.EnsureCoreWebView2Async(env);
            webView.CoreWebView2.Navigate("symantyx_canvas.html");

            webView.CoreWebView2.WebMessageReceived += async (s, e) =>
            {
                var msg = e.WebMessageAsJson;
                // Expect JSON like: { "action": "hydrate", "text": "...", "layer_id": "layer-001" }
                var response = await _http.PostAsync("http://localhost:8080/hydrate",
                    new StringContent(msg, Encoding.UTF8, "application/json"));
                var body = await response.Content.ReadAsStringAsync();
                await webView.CoreWebView2.ExecuteScriptAsync($"window.onHydrateResponse({body});");
            };
        }
    }
}
