using System;
using System.Collections.Concurrent;
using System.IO;
using System.Net.Http;
using System.Threading.Tasks;

using Avalonia.Media.Imaging;

namespace MoonPhaseApp;

public class ImageLoader
{
    private static readonly ConcurrentDictionary<string, Bitmap> _imageCache = new();

    public static async Task<Bitmap?> LoadFromWeb(Uri url)
    {
        if (_imageCache.TryGetValue(url.ToString(), out var cached))
            return cached;

        try
        {
            using var httpClient = new HttpClient();
            var response = await httpClient.GetAsync(url);
            response.EnsureSuccessStatusCode();
            var data = await response.Content.ReadAsByteArrayAsync();

            var bitmap = new Bitmap(new MemoryStream(data));
            _imageCache.TryAdd(url.ToString(), bitmap);
            return bitmap;
        }
        catch (HttpRequestException ex)
        {
            Console.WriteLine($"Error Loading Image: {url}, {ex.Message}");
            return null;
        }
    }
}