import customtkinter
import os
from PIL import Image
from typing import Optional


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Image Example")
        self.geometry("700x450")

        # Configure grid layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Initialize frames dictionary
        self.frames: Dict[str, customtkinter.CTkFrame] = {}
        
        # Load images
        self.images = self._load_images()
        
        # Create UI components
        self._create_navigation_frame()
        self._create_content_frames()
        
        # Select default frame
        self.select_frame_by_name("home")

    def _load_images(self) -> Dict[str, customtkinter.CTkImage]:
        """Load and return all required images with error handling."""
        try:
            image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")
            images = {
                "logo": customtkinter.CTkImage(
                    Image.open(os.path.join(image_path, "CustomTkinter_logo_single.png")),
                    size=(26, 26)
                ),
                "large_test": customtkinter.CTkImage(
                    Image.open(os.path.join(image_path, "large_test_image.png")),
                    size=(500, 150)
                ),
                "icon": customtkinter.CTkImage(
                    Image.open(os.path.join(image_path, "image_icon_light.png")),
                    size=(20, 20)
                ),
                "home": customtkinter.CTkImage(
                    light_image=Image.open(os.path.join(image_path, "home_dark.png")),
                    dark_image=Image.open(os.path.join(image_path, "home_light.png")),
                    size=(20, 20)
                ),
                "chat": customtkinter.CTkImage(
                    light_image=Image.open(os.path.join(image_path, "chat_dark.png")),
                    dark_image=Image.open(os.path.join(image_path, "chat_light.png")),
                    size=(20, 20)
                ),
                "add_user": customtkinter.CTkImage(
                    light_image=Image.open(os.path.join(image_path, "add_user_dark.png")),
                    dark_image=Image.open(os.path.join(image_path, "add_user_light.png")),
                    size=(20, 20)
                )
            }
            return images
        except Exception as e:
            print(f"Error loading images: {e}")
            return {}

    def _create_navigation_frame(self):
        """Create the navigation frame with buttons."""
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        # Navigation label
        self.navigation_frame_label = customtkinter.CTkLabel(
            self.navigation_frame,
            text="  Image Example",
            image=self.images.get("logo"),
            compound="left",
            font=customtkinter.CTkFont(size=15, weight="bold")
        )
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        # Navigation buttons
        nav_buttons = [
            ("Home", "home", self.images.get("home")),
            ("Frame 2", "frame_2", self.images.get("chat")),
            ("Frame 3", "frame_3", self.images.get("add_user"))
        ]

        for i, (text, frame_name, image) in enumerate(nav_buttons, 1):
            button = customtkinter.CTkButton(
                self.navigation_frame,
                corner_radius=0,
                height=40,
                border_spacing=10,
                text=text,
                fg_color="transparent",
                text_color=("gray10", "gray90"),
                hover_color=("gray70", "gray30"),
                image=image,
                anchor="w",
                command=lambda name=frame_name: self.select_frame_by_name(name)
            )
            button.grid(row=i, column=0, sticky="ew")
            setattr(self, f"{frame_name}_button", button)

        # Appearance mode menu
        self.appearance_mode_menu = customtkinter.CTkOptionMenu(
            self.navigation_frame,
            values=["Light", "Dark", "System"],
            command=self.change_appearance_mode_event
        )
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

    def _create_content_frames(self):
        """Create all content frames."""
        # Home frame
        self.frames["home"] = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.frames["home"].grid_columnconfigure(0, weight=1)
        
        # Add content to home frame
        self.home_frame_large_image_label = customtkinter.CTkLabel(
            self.frames["home"], text="", image=self.images.get("large_test")
        )
        self.home_frame_large_image_label.grid(row=0, column=0, padx=20, pady=10)

        for i in range(1, 5):
            button = customtkinter.CTkButton(
                self.frames["home"],
                text="CTkButton",
                image=self.images.get("icon"),
                compound=["", "right", "top", "bottom"][i-1]
            )
            button.grid(row=i, column=0, padx=20, pady=10)
            setattr(self, f"home_frame_button_{i}", button)

        # Other frames
        self.frames["frame_2"] = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.frames["frame_3"] = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

    def select_frame_by_name(self, name: str):
        """Select and display the specified frame."""
        # Update button colors
        for frame_name in ["home", "frame_2", "frame_3"]:
            button = getattr(self, f"{frame_name}_button")
            button.configure(fg_color=("gray75", "gray25") if frame_name == name else "transparent")

        # Show selected frame, hide others
        for frame_name, frame in self.frames.items():
            if frame_name == name:
                frame.grid(row=0, column=1, sticky="nsew")
            else:
                frame.grid_forget()

    def change_appearance_mode_event(self, new_appearance_mode: str):
        """Change the appearance mode of the application."""
        customtkinter.set_appearance_mode(new_appearance_mode)


if __name__ == "__main__":
    app = App()
    app.mainloop()
