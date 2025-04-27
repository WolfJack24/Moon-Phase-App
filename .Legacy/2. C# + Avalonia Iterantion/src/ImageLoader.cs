using System;
using System.Collections.Concurrent;
using System.IO;
using System.Net.Http;
using System.Threading.Channels;
using System.Threading.Tasks;

using Avalonia.Media.Imaging;

namespace MoonPhaseApp;

public class ImageLoader
{
    private static readonly ConcurrentDictionary<string, Bitmap> _imageCache = new();

    public static async void LoadFromWeb(ChannelWriter<Bitmap> writer, Uri url)
    {
        if (_imageCache.TryGetValue(url.ToString(), out var cached))
            writer.TryWrite(cached);

        try
        {
            using var httpClient = new HttpClient();
            var response = await httpClient.GetAsync(url);
            response.EnsureSuccessStatusCode();
            var data = await response.Content.ReadAsByteArrayAsync();

            var bitmap = new Bitmap(new MemoryStream(data));
            _imageCache.TryAdd(url.ToString(), bitmap);
            writer.TryWrite(bitmap);
        }
        catch (HttpRequestException ex)
        {
            Console.WriteLine($"Error Loading Image: {url}, {ex.Message}");
            return;
        }
        writer.Complete();
    }
}