using System;
using System.IO;
using System.Linq;
using System.Text.Json;
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

    private void GenerateImage_Click(object sender, RoutedEventArgs e)
    {
        Request rq = new();

        Task<string> DataTask = Task.Run(rq.GetImage);
        string data = DataTask.Result;

        if (data != string.Empty)
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
                Console.WriteLine(imageUrl);
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
    }
}
