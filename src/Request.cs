using System;
using System.Collections.Generic;
using System.Net;
using System.Net.Http;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;

namespace MoonPhaseApp;

public class Request
{
    private static readonly HttpClient client = new();

    public async Task<string> GetImage()
    {
        var request = new HttpRequestMessage(
            HttpMethod.Post,
            "https://api.astronomyapi.com/api/v2/studio/moon-phase"
        );

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

        List<string> secret = SetSecret.LoadSecret();

        if (secret.Count != 2)
        {
            return "13";
        }
        string Auth = Convert.ToBase64String(Encoding.UTF8.GetBytes($"{secret[0]}:{secret[1]}"));
        request.Headers.Add("Authorization", $"Basic {Auth}");

        var response = await client.SendAsync(request);

        HttpStatusCode status = response.StatusCode;
        if (status != HttpStatusCode.OK)
        {
            switch (status)
            {
                case HttpStatusCode.Forbidden:
#if DEBUG
                    Console.WriteLine(response);
#endif
                    return "";
                default:
                    return $"{Convert.ToInt32(status)}";
            }
        }

        return await response.Content.ReadAsStringAsync();
    }
}