using System;
using System.Diagnostics;

public class CPHInline
{
    public bool Execute()
    {
        Random rnd = new Random();
        int choice = rnd.Next(1, 101);
        string layerToVisible = "";
        string seatDisplay = "";

        switch (choice)
        {
            case int n when (n <= 60):
                layerToVisible = "Standing";
                seatDisplay = "GENERAL ADMISSION";
                break;

            case int n when (n > 90):
                layerToVisible = "Backstage";
                seatDisplay = "ALL ACCESS PASS";
                break;

            case int n when (n > 60 && n <=90):
                layerToVisible = "Seated";
                char row = (char)rnd.Next('A', 'Z' + 1);
                int seatNum = rnd.Next(1, 51);
                seatDisplay = $"Seat {row}{seatNum}";
                break;
        }

        CPH.SetArgument("ticketTypeLabel", layerToVisible);
        CPH.SetArgument("ticketSeatLabel", seatDisplay);

        return true;
    }
}
