using System;
using Avalonia;
using Avalonia.Controls;
using Avalonia.Interactivity;
using Avalonia.Markup.Xaml;
using Avalonia.Styling;


namespace MoonPhaseApp;

public partial class InfoWindow : Window
{
    public InfoWindow()
    {
        InitializeComponent();
    }

    private void InitializeComponent()
    {
        AvaloniaXamlLoader.Load(this);
    }

    private void UpdateInfo_Click(object sender, RoutedEventArgs e)
    {
    }

    protected override void OnClosing(WindowClosingEventArgs e)
    {
        base.OnClosing(e);

        Hide();
        e.Cancel = true;
    }

    private void TextBox_OnFocus(object? sender, RoutedEventArgs e)
    {
        if (sender is TextBox textBox)
        {
            //! WIP
            textBox.Text = "";
        }
    }

    private void TextBox_LostFocus(object? sender, RoutedEventArgs e)
    {
        if (sender is TextBox textBox)
        {
            string? name = textBox.Name;

            if (textBox.Text == string.Empty && name != null)
            {
                switch (name)
                {
                    case "BackgroundColor":
                        textBox.Text = "Background Colour";
                        break;
                    case "HeadingColor":
                        textBox.Text = "Heading Colour";
                        break;
                    case "TextColor":
                        textBox.Text = "Text Colour";
                        break;
                    case "Latitude":
                        textBox.Text = "Latitude";
                        break;
                    case "Longitude":
                        textBox.Text = "Longitude";
                        break;
                    case "Date":
                        textBox.Text = "YYYY-MM-DD";
                        break;
                }
            }
        }
    }
}
