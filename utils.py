def format_duration(seconds):
      hours = seconds // 3600  
      minutes = (seconds % 3600) // 60  
      seconds = (seconds % 3600) % 60  
      # Format the time string
      time_str = f"{hours:02}:{minutes:02}:{seconds:02}"
      return time_str