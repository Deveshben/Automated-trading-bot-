import yfinance
import pandas
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
import matplotlib.pyplot as plt
import io
import base64

def calculate_bollinger_bands(closing_prices, window=20, num_std_dev=2):
    moving_averages = []
    std_deviations = []
    upper_bands = []
    lower_bands = []

    for i in range(len(closing_prices) - window + 1):
        subset = closing_prices[i:i + window]
        moving_average = pandas.Series(subset).mean()
        std_deviation = pandas.Series(subset).std()
        upper_band = moving_average + num_std_dev * std_deviation
        lower_band = moving_average - num_std_dev * std_deviation

        moving_averages.append(moving_average)
        std_deviations.append(std_deviation)
        upper_bands.append(upper_band)
        lower_bands.append(lower_band)

    return moving_averages, std_deviations, upper_bands, lower_bands

class BollingerBandApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')

        # Add a dropdown list to select Indian shares
        dropdown = DropDown()
        symbols = ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "ITC.NS", "WIPRO.NS", "HINDUNILVR.NS", "ICICIBANK.NS",
                   "MARUTI.NS", "KOTAKBANK.NS", "TITAN.NS", "BAJAJFINSV.NS", "BHARTIARTL.NS", "AXISBANK.NS",
                   "ONGC.NS", "NTPC.NS", "POWERGRID.NS", "M&M.NS", "SUNPHARMA.NS", "NESTLEIND.NS", "HCLTECH.NS",
                   "COALINDIA.NS", "SBIN.NS", "LT.NS", "IOC.NS", "BAJFINANCE.NS", "JSWSTEEL.NS", "ULTRACEMCO.NS",
                   "BRITANNIA.NS", "DRREDDY.NS", "ASIANPAINT.NS", "HEROMOTOCO.NS", "TECHM.NS", "GRASIM.NS",
                   "EICHERMOT.NS", "INDUSINDBK.NS", "SHREECEM.NS", "CIPLA.NS", "VEDL.NS", "DIVISLAB.NS",
                   "ADANIPORTS.NS", "TATAMOTORS.NS", "RELIANCE.NS", "ITC.NS", "INFY.NS", "TCS.NS", "HDFCBANK.NS",
                   "HINDUNILVR.NS", "ICICIBANK.NS", "MARUTI.NS", "KOTAKBANK.NS", "TITAN.NS", "BAJAJFINSV.NS",
                   "BHARTIARTL.NS", "AXISBANK.NS", "ONGC.NS", "NTPC.NS", "POWERGRID.NS", "M&M.NS", "SUNPHARMA.NS",
                   "NESTLEIND.NS", "HCLTECH.NS", "COALINDIA.NS", "SBIN.NS", "LT.NS", "IOC.NS", "BAJFINANCE.NS",
                   "JSWSTEEL.NS", "ULTRACEMCO.NS", "BRITANNIA.NS", "DRREDDY.NS", "ASIANPAINT.NS", "HEROMOTOCO.NS",
                   "TECHM.NS", "GRASIM.NS", "EICHERMOT.NS", "INDUSINDBK.NS", "SHREECEM.NS", "CIPLA.NS", "VEDL.NS",
                   "DIVISLAB.NS", "ADANIPORTS.NS", "TATAMOTORS.NS", "RELIANCE.BO", "ITC.BO", "INFY.BO", "TCS.BO",
                   "HDFCBANK.BO", "HINDUNILVR.BO", "ICICIBANK.BO", "MARUTI.BO", "KOTAKBANK.BO", "TITAN.BO",
                   "BAJAJFINSV.BO", "BHARTIARTL.BO", "AXISBANK.BO", "ONGC.BO", "NTPC.BO", "POWERGRID.BO",
                   "M&M.BO", "SUNPHARMA.BO", "NESTLEIND.BO", "HCLTECH.BO", "COALINDIA.BO", "SBIN.BO", "LT.BO",
                   "IOC.BO", "BAJFINANCE.BO", "JSWSTEEL.BO", "ULTRACEMCO.BO", "BRITANNIA.BO", "DRREDDY.BO",
                   "ASIANPAINT.BO", "HEROMOTOCO.BO", "TECHM.BO", "GRASIM.BO", "EICHERMOT.BO", "INDUSINDBK.BO",
                   "SHREECEM.BO", "CIPLA.BO", "VEDL.BO", "DIVISLAB.BO", "ADANIPORTS.BO", "TATAMOTORS.BO"]

        for symbol in symbols:
            btn = Button(text=symbol, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: dropdown.select(btn.text))
            dropdown.add_widget(btn)

        main_button = Button(text='Select Share', size_hint=(1, 0.1))
        main_button.bind(on_release=dropdown.open)
        dropdown.bind(on_select=self.on_share_selected)

        layout.add_widget(main_button)

        # Add an Image widget to display the graph
        self.graph_image = Image(source='', size_hint=(1, 0.9))
        layout.add_widget(self.graph_image)

        return layout

    def on_share_selected(self, instance, value):
        # When the user selects a share from the dropdown, update the graph
        stock = yfinance.Ticker(value)
        data = stock.history(period="30d")
        closing_prices = data["Close"].tolist()

        # Store the Bollinger Bands results in a tuple
        bands_data = calculate_bollinger_bands(closing_prices)

        # Unpack the tuple into separate lists
        moving_averages, std_deviations, upper_bands, lower_bands = bands_data

        # Create a new figure for the selected share
        fig, ax = plt.subplots()

        # Plot the Bollinger Bands on the figure
        subset_range = range(len(moving_averages))
        ax.plot(subset_range, moving_averages, color='red', label='Moving Average')
        ax.plot(subset_range, upper_bands, color='green', label='Upper Band')
        ax.plot(subset_range, lower_bands, color='blue', label='Lower Band')

        ax.set_xlabel('Subset')
        ax.set_ylabel('Value')
        ax.set_title(f'Bollinger Bands for {value}')
        ax.legend()

        # Save the plot as a PNG image in bytes
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        plt.close()

        # Convert the image buffer to base64 string
        buffer_str = base64.b64encode(buffer.read()).decode()

        # Update the Kivy Image widget with the new graph
        self.graph_image.source = f'data:image/png;base64,{buffer_str}'

if __name__ == '__main__':
    BollingerBandApp().run()
