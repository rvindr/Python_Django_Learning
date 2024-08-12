
from .models import Products, Brand
from faker import Faker
import random

def handle():
        faker = Faker()

        categories = ['Electronics', 'Mobiles', 'Computer', 'Clothes', 'Toys', 'Grocery']
        brands = Brand.objects.all()
        product_names = [
    "UltraSlim LED TV", "EcoFriendly Water Bottle", "Smartphone Pro X", "Noise Cancelling Headphones", 
    "Wireless Bluetooth Speaker", "Portable Power Bank", "High-Performance Laptop", "Smart Home Hub", 
    "Gaming Console Elite", "Wireless Earbuds", "4K Action Camera", "Bluetooth Fitness Tracker", 
    "Rechargeable Electric Toothbrush", "Solar Powered Charger", "Smart Thermostat", "Voice-Activated Assistant", 
    "Virtual Reality Headset", "Noise-Isolating Earphones", "Portable Air Purifier", "Digital Kitchen Scale", 
    "Electric Kettle", "Smart Coffee Maker", "Robot Vacuum Cleaner", "Smart Light Bulb", 
    "Wireless Charging Pad", "Home Security Camera", "Ergonomic Office Chair", "Smart Doorbell", 
    "Waterproof Smartwatch", "Digital Picture Frame", "Programmable Pressure Cooker", "Smart WiFi Router", 
    "Electric Standing Desk", "High-Speed Blender", "Smart Alarm Clock", "Portable Projector", 
    "Cordless Vacuum Cleaner", "Automatic Pet Feeder", "Wireless Gaming Mouse", "Smart Plugs", 
    "Wireless Keyboard", "Adjustable Dumbbells", "Smart Bike Helmet", "Wireless Baby Monitor", 
    "Portable Camping Stove", "Noise-Canceling Mic", "Smart Refrigerator", "Digital Meat Thermometer", 
    "Wireless Doorbell", "Smart Light Strip", "Electric Hair Trimmer", "WiFi Range Extender", 
    "Electric Foot Massager", "Smart Body Scale", "Portable Fire Pit", "Smart Window Blinds", 
    "Digital Audio Recorder", "Foldable Drone", "Electric Heated Blanket", "Wireless Home Theater System", 
    "Smart Smoke Detector", "Cordless Drill", "Solar Garden Lights", "Portable Mini Fridge", 
    "Electric Scooter", "Smart Door Lock", "Digital Air Fryer", "Wireless Charger", 
    "Smart Yoga Mat", "Bluetooth Sleep Mask", "Electric Bike", "Voice-Controlled Speaker", 
    "Smart Ceiling Fan", "Wireless HDMI Transmitter", "Electric Wine Opener", "Smart Pet Camera", 
    "Noise-Isolating Headset", "Portable Jump Starter", "Waterproof Action Camera", "Wireless Charging Stand", 
    "Smart Fitness Bike", "Digital Luggage Scale", "Electric Pressure Washer", "Smart Sprinkler System", 
    "Solar Lantern", "Wireless Meat Thermometer", "Electric Warming Tray", "Bluetooth Shower Speaker", 
    "Smart Mirror", "Digital Blood Pressure Monitor", "Wireless Dog Fence", "Smart Irrigation Controller", 
    "Portable Folding Table", "Electric Scooter Pro", "Wireless Car Charger", "Smart Wine Fridge", 
    "Portable Bluetooth Keyboard", "Electric Heated Gloves", "Digital Piano", "Wireless Lavalier Microphone", 
    "Smart Mug", "Bluetooth Car Kit", "Electric Razor", "Smart Bike Lock",
    "Smart Fitness Tracker", "Air Purifier with HEPA Filter", "Portable Blender", 
    "High-Definition Webcam", "Smart Light Switch", "Electric Wine Cooler", 
    "Digital Instant Read Thermometer", "Multi-Function Rice Cooker", 
    "Smart Lock for Front Door", "High-Resolution Drone Camera", 
    "Adjustable Desk Lamp", "Portable Air Conditioner", 
    "Wireless Noise-Cancelling Headphones", "Smart Wi-Fi Camera", 
    "Electric Milk Frother", "Digital Voice Recorder", "Smart Garden System", 
    "Wireless Smart Plug", "Compact Sous Vide Machine", 
    "Automated Pet Door", "Bluetooth Thermal Printer", 
    "Portable Power Generator", "Smart Wi-Fi Water Sensor", 
    "Digital Measuring Cup", "Electric Slicer", 
    "Smart Wi-Fi Smoke Detector", "Automatic Cat Litter Box", 
    "High-Performance Food Processor", "Smart Water Bottle with Hydration Tracker", 
    "Compact Cordless Iron", "LED Desk Organizer with Wireless Charger", 
    "Smart Home Humidifier", "Foldable Electric Scooter", 
    "Wireless Bluetooth Car Stereo", "High-Speed Wireless Router", 
    "Digital Hair Styling Tool", "Smart Refrigerator with Touch Screen", 
    "Cordless Handheld Vacuum Cleaner", "Adjustable Portable Tripod", 
    "Smart Home Air Quality Monitor", "Wireless Home Intercom System", 
    "Smart Irrigation System", "Digital Keyless Entry Lock", 
    "Bluetooth Enabled Food Scale", "Portable Induction Cooktop", 
    "Smart Thermostat with Voice Control", "Wireless Smart Watering System", 
    "Electric Multi-Cooker", "Smart Home Security System", 
    "Compact Air Fryer"
]


        for name in product_names:  # Iterate through the product names
            image_url = f"https://picsum.photos/200/300?random={random.randint(1, 1000)}"

            product = Products.objects.create(
                title=name,
                image=image_url,
                category=random.choice(categories),
                description=faker.text(),
                brand_name=random.choice(brands),
                sku=faker.ean8()
            )

