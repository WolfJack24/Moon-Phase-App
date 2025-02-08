using System;
using System.Collections.Generic;
using System.IO;
using System.Net;
using System.Net.Http;
using System.Text;
using System.Text.Json;
using System.Threading.Channels;
using System.Threading.Tasks;

namespace MoonPhaseApp;

public class Request
{
    private static readonly HttpClient client = new();

    public static async Task GetImage(ChannelWriter<string> writer)
    {
        string data;
        var request = new HttpRequestMessage(
            HttpMethod.Post,
            "https://api.astronomyapi.com/api/v2/studio/moon-phase"
        );
        Console.WriteLine("[class Request] Setup request");

        string Body = JsonSerializer.Serialize(new
        {
            format = Constants.DefualtFormat,
            style = new
            {
                moonStyle = Constants.DefaultMoonstyle,
                backgroundStyle = Constants.DefaultBackgroundStyle,
                backgroundColor = Constants.DefaultBackgroundColour,
                headingColor = Constants.DefaultHeadingColour,
                textColor = Constants.DefaultTextColour,
            },
            observer = new
            {
                latitude = Constants.DefaultLatitude,
                longitude = Constants.DefaultLatitude,
                date = Constants.DefaultDate
            },
            view = new
            {
                type = Constants.DefaultType,
                orientation = Constants.DefaultOrientation,
            },
        });
        request.Content = new StringContent(Body);
        Console.WriteLine("[class Request] Setup body");

        List<string> secret = SetSecret.LoadSecret();

        if (secret.Count != 2)
        {
            data = "13";
        }
        string Auth = Convert.ToBase64String(Encoding.UTF8.GetBytes($"{secret[0]}:{secret[1]}"));
        request.Headers.Add("Authorization", $"Basic {Auth}");
        Console.WriteLine("[class Request] Setup auth");

        var response = await client.SendAsync(request);
        Console.WriteLine("[class Request] Sent request");

        HttpStatusCode status = response.StatusCode;
        if (status != HttpStatusCode.OK)
        {
            switch (status)
            {
                case HttpStatusCode.Forbidden:
#if DEBUG
                    Console.WriteLine(response);
#endif
                    data = "";
                    break;
                default:
                    data = $"{Convert.ToInt32(status)}";
                    break;
            }
        }

        data = await response.Content.ReadAsStringAsync();
        Console.WriteLine($"[class Request] Got response: {data}");
        if (!writer.TryWrite(data))
        {
            Console.WriteLine("Error: Could not write to the Channel.");
        }
        writer.Complete();
    }
}