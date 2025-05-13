package main

import (
	"log"
	"strconv"
	"strings"

	"github.com/wailsapp/wails/v3/pkg/application"
)

type ColourService struct{}

// TODO: Figure out how to use these colours in the frontend
// * a struct seems painful, and enum has a weird syntax - another days problem

type Colour int

const (
	TextColour Colour = iota
	WindowBackgroundColour
	FrameBackgroundColour
	ButtonBackgroundColour
	ButtonHoverColour
	ButtonTextColour
	LabelTextColour
	EntryBackgroundColour
	EntryBorderColour
	EntryTextColour
	EntryPlaceholderColour
	ComboboxBackgroundColour
	ComboboxBorderColour
	ComboboxHoverColour
	ComboboxTextColour
	ColourCount
)

// ? All clours are from blue.json from CustomTkinter
// ? But in hex format from:
// ? https://github.com/WolfJack24/Morse-Code-Translator/blob/main/assets/theme/blue_in_hex.json
const (
	Text = "#DCE4EE"

	// Windows
	WindowBackground = "#242424"

	// Frames i.e <divs>
	FrameBackground = "#2B2B2B"

	// Buttons
	ButtonBackground = "#1F6AA5"
	ButtonHover      = "#144870"
	ButtonText       = Text

	// Text/Labels
	LabelText = Text

	// Entry i.e <input> fields
	EntryBackground  = "#343638"
	EntryBorder      = "#565B5E"
	EntryText        = Text
	EntryPlaceholder = "#9E9E9E"

	// Don't use Checkboxes, Switches, Radiobuttons, Progressbars, Sliders, OptionMenus

	// Comboboxes
	ComboboxBackground = "#343638"
	ComboboxBorder     = "#565B5E"
	ComboboxHover      = "#7A848D"
	ComboboxText       = Text

	// Don't use Scrollbars, SegmentedButton, Textbox, ScrollableFrame and DropdownMenus
)

func (c *ColourService) HexToRGB(hex string) application.RGBA {
	// Remove the '#' character
	hex = strings.TrimPrefix(hex, "#")

	// Convert string to integers
	hexvalue, err := strconv.ParseInt(hex, 16, 32)
	if err != nil {
		log.Fatal("Error: ", err)
	}

	// Extract the RGB values from the hex value
	var r, g, b uint8
	r = uint8(((hexvalue >> 16) & 0xFF))
	g = uint8(((hexvalue >> 8) & 0xFF))
	b = uint8((hexvalue & 0xFF))

	return application.RGBA{
		Red:   r,
		Green: g,
		Blue:  b,
		Alpha: 0xFF,
	}
}

func (c *ColourService) GetColour(colour Colour) string {
	switch colour {
	case TextColour:
		{
			return Text
		}
	case WindowBackgroundColour:
		{
			return WindowBackground
		}
	case FrameBackgroundColour:
		{
			return FrameBackground
		}
	case ButtonBackgroundColour:
		{
			return ButtonBackground
		}
	case ButtonHoverColour:
		{
			return ButtonHover
		}
	case ButtonTextColour:
		{
			return ButtonText
		}
	case LabelTextColour:
		{
			return LabelText
		}
	case EntryBackgroundColour:
		{
			return EntryBackground
		}
	case EntryBorderColour:
		{
			return EntryBorder
		}
	case EntryTextColour:
		{
			return EntryText
		}
	case EntryPlaceholderColour:
		{
			return EntryPlaceholder
		}
	case ComboboxBackgroundColour:
		{
			return ComboboxBackground
		}
	case ComboboxBorderColour:
		{
			return ComboboxBorder
		}
	case ComboboxHoverColour:
		{
			return ComboboxHover
		}
	case ComboboxTextColour:
		{
			return ComboboxText
		}
	}
	return "#000" // Default to black if no match found
}
