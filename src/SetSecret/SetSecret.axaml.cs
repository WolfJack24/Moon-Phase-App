using System;
using System.Collections.Generic;
using System.IO;
using System.Text;

using Avalonia.Controls;
using Avalonia.Interactivity;
using Avalonia.Markup.Xaml;

namespace MoonPhaseApp;

public partial class SetSecret : Window
{
    public SetSecret()
    {
        InitializeComponent();
    }

    private void InitializeComponent()
    {
        AvaloniaXamlLoader.Load(this);
    }

    protected override void OnOpened(EventArgs e)
    {
        base.OnOpened(e);
    }

    protected override void OnClosing(WindowClosingEventArgs e)
    {
        base.OnClosing(e);

        Hide();
        e.Cancel = true;
    }

    private void Save_Click(object? sender, RoutedEventArgs e)
    {
        var appIdTextBox = this.FindControl<TextBox>("AppID");
        var appSecretTextBox = this.FindControl<TextBox>("AppSecret");

        if (appIdTextBox is null || appSecretTextBox is null)
        {
            throw new NullReferenceException("App ID or App Secret text box is null.");
        }

        string? ID = appIdTextBox.Text ?? "";
        string? Secret = appSecretTextBox.Text ?? "";

        if (!Directory.Exists(Constants.FileDir))
        {
            Directory.CreateDirectory(Constants.FileDir);
        }

        if (!string.IsNullOrEmpty(ID) && ID != "App ID" &&
            !string.IsNullOrEmpty(Secret) && Secret != "App Secret")
        {
            using var stream = File.Open(Constants.FileName, FileMode.Create);
            using var writer = new BinaryWriter(stream, Encoding.Unicode, false);

            writer.Write(ID);
            writer.Write(Secret);

            Console.WriteLine("Secret saved.");
            Hide();
        }
        else
        {
            Console.WriteLine("Please enter a valid App ID and App Secret.");
        }
    }

    public static List<string> LoadSecret()
    {
        if (File.Exists(Constants.FileName))
        {
            using var stream = File.Open(Constants.FileName, FileMode.Open);
            using var reader = new BinaryReader(stream, Encoding.Unicode, false);

            return
            [
                reader.ReadString(),
                reader.ReadString()
            ];
        }

        return [];
    }

    private void Secret_OnFocus(object? sender, RoutedEventArgs e)
    {
        if (sender is TextBox textBox)
        {
            string? name = textBox.Name;

            if (name != null)
            {
                switch (name)
                {
                    case "AppID":
                        if (textBox.Text == "App ID")
                        {
                            textBox.Text = "";
                        }
                        break;
                    case "AppSecret":
                        if (textBox.Text == "App Secret")
                        {
                            textBox.Text = "";
                        }
                        break;
                }
            }
        }
    }

    private void Secret_LostFocus(object? sender, RoutedEventArgs e)
    {
        if (sender is TextBox textBox)
        {
            string? name = textBox.Name;

            if (textBox.Text == string.Empty && name != null)
            {
                switch (name)
                {
                    case "AppID":
                        textBox.Text = "App ID";
                        break;
                    case "AppSecret":
                        textBox.Text = "App Secret";
                        break;
                }
            }
        }
    }
}



