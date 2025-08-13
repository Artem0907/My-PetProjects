import tkinter
import tkinter.messagebox
from typing import Any, Optional, Union
import customtkinter as ctk

# Configure appearance
ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(ctk.CTk):
    """Main application class for the CustomTkinter example.
    
    This class creates a complex example application with various widgets and features
    to demonstrate the capabilities of CustomTkinter.
    """
    
    def __init__(self) -> None:
        """Initialize the application with default settings and create the UI."""
        super().__init__()
        
        # Configure window
        self.title("[CustomTkinter] complex example")
        self.geometry(f"{1100}x{580}")
        
        # Configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)
        
        # Initialize UI components
        self._create_sidebar()
        self._create_main_content()
        self._create_tabview()
        self._create_radiobutton_frame()
        self._create_slider_progressbar_frame()
        self._create_scrollable_frame()
        self._create_checkbox_frame()
        
        # Set default values
        self._set_default_values()

    def _create_sidebar(self) -> None:
        """Create the sidebar frame with widgets."""
        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        
        # Logo label
        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame,
            text="CustomTkinter",
            font=ctk.CTkFont(size=20, weight="bold"),
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        # Sidebar buttons
        for i in range(1, 4):
            button = ctk.CTkButton(
                self.sidebar_frame,
                command=self.sidebar_button_event,
                text=f"Button {i}"
            )
            button.grid(row=i, column=0, padx=20, pady=10)
            setattr(self, f"sidebar_button_{i}", button)
        
        # Appearance mode
        self.appearance_mode_label = ctk.CTkLabel(
            self.sidebar_frame, text="Appearance Mode:", anchor="w"
        )
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(
            self.sidebar_frame,
            values=["Light", "Dark", "System"],
            command=self.change_appearance_mode_event,
        )
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        
        # UI Scaling
        self.scaling_label = ctk.CTkLabel(
            self.sidebar_frame, text="UI Scaling:", anchor="w"
        )
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        
        self.scaling_optionemenu = ctk.CTkOptionMenu(
            self.sidebar_frame,
            values=["80%", "90%", "100%", "110%", "120%"],
            command=self.change_scaling_event,
        )
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

    def _create_main_content(self) -> None:
        """Create the main content area with entry and button."""
        self.entry = ctk.CTkEntry(self, placeholder_text="CTkEntry")
        self.entry.grid(
            row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew"
        )
        
        self.main_button_1 = ctk.CTkButton(
            master=self,
            fg_color="transparent",
            border_width=2,
            text_color=("gray10", "#DCE4EE"),
            text="Main Button"
        )
        self.main_button_1.grid(
            row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew"
        )
        
        self.textbox = ctk.CTkTextbox(self, width=250)
        self.textbox.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")

    def _create_tabview(self) -> None:
        """Create the tabview with multiple tabs."""
        self.tabview = ctk.CTkTabview(self, width=250)
        self.tabview.grid(row=0, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        
        # Add tabs
        self.tabview.add("CTkTabview")
        self.tabview.add("Tab 2")
        self.tabview.add("Tab 3")
        
        # Configure grid for tabs
        self.tabview.tab("CTkTabview").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Tab 2").grid_columnconfigure(0, weight=1)
        
        # Add widgets to first tab
        self.optionmenu_1 = ctk.CTkOptionMenu(
            self.tabview.tab("CTkTabview"),
            dynamic_resizing=False,
            values=["Value 1", "Value 2", "Value Long Long Long"],
        )
        self.optionmenu_1.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        self.combobox_1 = ctk.CTkComboBox(
            self.tabview.tab("CTkTabview"),
            values=["Value 1", "Value 2", "Value Long....."],
        )
        self.combobox_1.grid(row=1, column=0, padx=20, pady=(10, 10))
        
        self.string_input_button = ctk.CTkButton(
            self.tabview.tab("CTkTabview"),
            text="Open CTkInputDialog",
            command=self.open_input_dialog_event,
        )
        self.string_input_button.grid(row=2, column=0, padx=20, pady=(10, 10))
        
        # Add label to second tab
        self.label_tab_2 = ctk.CTkLabel(
            self.tabview.tab("Tab 2"), text="CTkLabel on Tab 2"
        )
        self.label_tab_2.grid(row=0, column=0, padx=20, pady=20)

    def _create_radiobutton_frame(self) -> None:
        """Create the radiobutton frame with radio buttons."""
        self.radiobutton_frame = ctk.CTkFrame(self)
        self.radiobutton_frame.grid(
            row=0, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew"
        )
        
        self.radio_var = tkinter.IntVar(value=0)
        self.label_radio_group = ctk.CTkLabel(
            master=self.radiobutton_frame, text="CTkRadioButton Group:"
        )
        self.label_radio_group.grid(
            row=0, column=2, columnspan=1, padx=10, pady=10, sticky=""
        )
        
        for i in range(1, 4):
            radio_button = ctk.CTkRadioButton(
                master=self.radiobutton_frame,
                variable=self.radio_var,
                value=i-1,
                text=f"Radio {i}"
            )
            radio_button.grid(row=i, column=2, pady=10, padx=20, sticky="n")
            setattr(self, f"radio_button_{i}", radio_button)

    def _create_slider_progressbar_frame(self) -> None:
        """Create the slider and progressbar frame."""
        self.slider_progressbar_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.slider_progressbar_frame.grid(
            row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew"
        )
        self.slider_progressbar_frame.grid_columnconfigure(0, weight=1)
        self.slider_progressbar_frame.grid_rowconfigure(4, weight=1)
        
        # Segmented button
        self.seg_button_1 = ctk.CTkSegmentedButton(self.slider_progressbar_frame)
        self.seg_button_1.grid(
            row=0, column=0, padx=(20, 10), pady=(10, 10), sticky="ew"
        )
        
        # Progress bars
        for i in range(1, 3):
            progressbar = ctk.CTkProgressBar(self.slider_progressbar_frame)
            progressbar.grid(
                row=i, column=0, padx=(20, 10), pady=(10, 10), sticky="ew"
            )
            setattr(self, f"progressbar_{i}", progressbar)
        
        # Sliders
        self.slider_1 = ctk.CTkSlider(
            self.slider_progressbar_frame, from_=0, to=1, number_of_steps=4
        )
        self.slider_1.grid(row=3, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        
        self.slider_2 = ctk.CTkSlider(
            self.slider_progressbar_frame, orientation="vertical"
        )
        self.slider_2.grid(
            row=0, column=1, rowspan=5, padx=(10, 10), pady=(10, 10), sticky="ns"
        )
        
        self.progressbar_3 = ctk.CTkProgressBar(
            self.slider_progressbar_frame, orientation="vertical"
        )
        self.progressbar_3.grid(
            row=0, column=2, rowspan=5, padx=(10, 20), pady=(10, 10), sticky="ns"
        )

    def _create_scrollable_frame(self) -> None:
        """Create the scrollable frame with switches."""
        self.scrollable_frame = ctk.CTkScrollableFrame(
            self, label_text="CTkScrollableFrame"
        )
        self.scrollable_frame.grid(
            row=1, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew"
        )
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        
        self.scrollable_frame_switches = []
        for i in range(100):
            switch = ctk.CTkSwitch(
                master=self.scrollable_frame, text=f"CTkSwitch {i}"
            )
            switch.grid(row=i, column=0, padx=10, pady=(0, 20))
            self.scrollable_frame_switches.append(switch)

    def _create_checkbox_frame(self) -> None:
        """Create the checkbox and switch frame."""
        self.checkbox_slider_frame = ctk.CTkFrame(self)
        self.checkbox_slider_frame.grid(
            row=1, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew"
        )
        
        for i in range(1, 4):
            checkbox = ctk.CTkCheckBox(master=self.checkbox_slider_frame)
            checkbox.grid(row=i, column=0, pady=(20, 0), padx=20, sticky="n")
            setattr(self, f"checkbox_{i}", checkbox)

    def _set_default_values(self) -> None:
        """Set default values for widgets."""
        self.sidebar_button_3.configure(state="disabled", text="Disabled CTkButton")
        self.checkbox_3.configure(state="disabled")
        self.checkbox_1.select()
        self.scrollable_frame_switches[0].select()
        self.scrollable_frame_switches[4].select()
        self.radio_button_3.configure(state="disabled")
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")
        self.optionmenu_1.set("CTkOptionmenu")
        self.combobox_1.set("CTkComboBox")
        self.slider_1.configure(command=self.progressbar_2.set)
        self.slider_2.configure(command=self.progressbar_3.set)
        self.progressbar_1.configure(mode="indeterminate")
        self.progressbar_1.start()
        self.textbox.insert(
            "0.0",
            "CTkTextbox\n\n"
            + "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.\n\n"
            * 20,
        )
        self.seg_button_1.configure(values=["CTkSegmentedButton", "Value 2", "Value 3"])
        self.seg_button_1.set("Value 2")

    def open_input_dialog_event(self) -> None:
        """Open an input dialog and print the result."""
        dialog = ctk.CTkInputDialog(
            text="Type in a number:", title="CTkInputDialog"
        )
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str) -> None:
        """Change the appearance mode of the application.
        
        Args:
            new_appearance_mode: The new appearance mode to set.
        """
        ctk.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str) -> None:
        """Change the UI scaling of the application.
        
        Args:
            new_scaling: The new scaling percentage to set.
        """
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self) -> None:
        """Handle sidebar button click events."""
        print("sidebar_button click")


if __name__ == "__main__":
    app = App()
    app.mainloop()
