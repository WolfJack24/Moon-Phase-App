package main

type PayloadService struct{}

type Payload struct {
	// Format
	Format string

	// Style
	MoonStyle        string
	BackgroundStyle  string
	BackgroundColour string
	HeadingColour    string
	TextColour       string

	// Observer
	Latitude  float32
	Longitude float32
	Date      string

	// View
	Type        string
	Orientation string
}

func (p *PayloadService) CreatePayload() Payload {
	return Payload{
		Format:           "png",
		MoonStyle:        "default",
		BackgroundStyle:  "stars",
		BackgroundColour: "black",
		HeadingColour:    "white",
		TextColour:       "white",
		Latitude:         6.56774,
		Longitude:        79.88956,
		Date:             "2024-07-18",
		Type:             "portrait-simple",
		Orientation:      "south-up",
	}
}