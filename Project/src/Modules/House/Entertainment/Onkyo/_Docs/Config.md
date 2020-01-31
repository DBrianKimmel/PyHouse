
## config file onkyo.yaml

```
Onkyo:
    Name: Onkyo components
    Comment: The Onkyo A/V device
    Devices:
        - Name: Onkyo A/V Receiver
          Comment: Main Receiver
          Host:
              Name: onkyo-01-pp
              Port: 8102
          Type: Receiver
          Model: TX-555
        - Name: Onkyo Device 2
          Comment: Bedroom Receiver
          Host:
              Name: onkyo-02-pp
              Port: 8102
          Type: Receiver
          Model: TX-567
```