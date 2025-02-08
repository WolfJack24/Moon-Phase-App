using System;
using System.IO;
using System.Linq;
using System.Text.Json;
using System.Threading;
using System.Threading.Channels;
using System.Threading.Tasks;

using Avalonia.Controls;
using Avalonia.Interactivity;
using Avalonia.Media.Imaging;

namespace MoonPhaseApp;

public partial class MainWindow : Window
{
    InfoWindow? _infoWindow = new();
    SetSecret? _setSecret = new();

    public MainWindow()
    {
        InitializeComponent();
    }

    override protected void OnOpened(EventArgs e)
    {
        base.OnOpened(e);

        if (!File.Exists(Constants.FileName))
        {
            _setSecret?.Show();
        }
    }

    protected override void OnClosed(EventArgs e)
    {
        base.OnClosed(e);

        _setSecret?.Close();
        _setSecret = null;
        _infoWindow?.Close();
        _infoWindow = null;
        // ? If run in terminal it does not finish the "process" so we call Exit
        Environment.Exit(0);
    }

    private void SetInfo_Click(object sender, RoutedEventArgs e)
    {
        _infoWindow?.Show();
    }

    private async void ImageStuff()
    {
        Channel<string> getImageChannel = Channel.CreateUnbounded<string>();
        Channel<Bitmap> imageChannel = Channel.CreateUnbounded<Bitmap>();

        await Request.GetImage(getImageChannel.Writer);

        if (!getImageChannel.Reader.TryRead(out string? data))
        {
            Console.WriteLine("Error: No data returned from the Channel.");
        }

        if (data != string.Empty && data != null)
        {
            if (data == "13")
            {
                Console.WriteLine("No Secret, Press <F1> to bring up the Secrets Window.");
            }
            else if (data.All(char.IsDigit))
            {
                Console.WriteLine($"Error: {data}");
                return;
            }

            var jsonDoc = JsonDocument.Parse(data);
            if (jsonDoc.RootElement.TryGetProperty("data", out JsonElement dataElement) &&
                dataElement.TryGetProperty("imageUrl", out JsonElement imageUrlElement))
            {
                var imageUrl = imageUrlElement.GetString();
                if (imageUrl != null)
                {
                    Console.WriteLine("Loading Image...");
                    Thread imageThread = new(
                        new ThreadStart(() => ImageLoader.LoadFromWeb(imageChannel.Writer, new Uri(imageUrl))));
                    imageThread.Start();
                    imageThread.Join();
                }
                else
                {
                    Console.WriteLine("Error: Image URL is null.");
                    return;
                }

                var image = await imageChannel.Reader.ReadAsync();
                //? This program will crash from this point as it is calling Image which if know how Threads work
                //? it should be Thread[0] but this function get called in a new Thread => Thread[1]
                //? in othercase - if i am correct - it is basically a null pointer => 0x0000...
                Image.Source = image ?? new Bitmap($"{Constants.AssetsPath}/Icons/icon.png");
                Console.WriteLine("Image Loaded.");
            }
            else
            {
                Console.WriteLine("Error: 'imageUrl' key not found in the JSON response.");
                foreach (var prop in jsonDoc.RootElement.EnumerateObject())
                {
                    Console.WriteLine($"Found property: {prop.Name}");
                }
            }
        }
        else
        {
            Console.WriteLine("Error: Data returned from the Channel but was null.");
        }
    }

    private void GenerateImage_Click(object sender, RoutedEventArgs e)
    {
        Thread thread = new(ImageStuff);
        thread.Start();
    }
}
