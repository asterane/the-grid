

<a id="org1affdc0"></a>

# The Grid

![img](./media/pictures/first_light_crop.jpg)


# Table of Contents

1.  [Under Construction](#org36e0b87)
2.  [Overview](#org138f860)
3.  [Project Goals](#org91b989c)
    1.  [Overall](#org6f5a60e)
    2.  [Design](#org069cb31)
    3.  [Implementation](#org06c6ddf)
4.  [System](#org722d198)
5.  [Structure](#orgebfdcf1)
6.  [Electronics](#org42d862f)
7.  [Software](#orgb3229b2)
8.  [Reflection](#org93f03fa)


<a id="org36e0b87"></a>

# Under Construction

This readme file will become much more extensive in the future.


<a id="org138f860"></a>

# Overview

// Convert to paragraphs

-   We built a display wall composed of 60 wooden cubes, each containing
    four high power RGB LEDs and acting as a pixel
-   This project was part of an ambitious set for a high school production of
    The Curious Incident of the Dog in the Night-time
-   The system had many aspects, most of which I designed myself, and
    oversaw the implementation of
    -   Each cube was a frame built out of 2 by 4 lumber, with a mounting
        panel in the middle and diffusing plastic on the front
    -   Four high power LEDs were installed in each cube; all four in any
        cube would always be the same color
    -   Current had to be supplied to the LEDs, so we built and connected
        circuit boards by hand to drive them
    -   Power for the circuit boards came from power supplies that we
        wired and fused ourselves
    -   Four Arduino microcontrollers controlled the brightness of 240
        LEDs, and were in turn controlled by a Raspberry Pi
    -   Custom software to set the sequence of lights for the show ran on
        my laptop, connected to the Pi
-   As well as the design and implementation, I also managed the finding
    and acquisition of every component we needed
-   After three months of work, the Grid was completed on time and as
    specified, ready for the show
-   The Grid was used for all four performances of our production,
    providing a powerful backdrop for the characters
-   Our show was commended by critics for the technical feat, and we
    would have won one of the region wide high school theatrical awards
    for it had school not been canceled in March
-   While I was the lead engineer, I also worked with a team of great
    people, without whom this project would not have been possible
-   One colleague of mine contributed more than any other, personally
    writing thousands of lines of code to create the Grid client
    software, for which I give her full credit


<a id="org91b989c"></a>

# Project Goals


<a id="org6f5a60e"></a>

## Overall

-   Build a huge, visually striking set piece with dynamic lighting
    elements to serve as the backdrop for a play
-   Display a sequence of designs during the show, including static
    images and animations
-   Surprise the audience with the breadth and scale of effects that may
    be shown on the display
-   Enhance immersion in the show by making the backdrop designs, and
    the piece itself, fit a certain aesthetic
-   Learn valuable techniques for multidisciplinary engineering and
    project management
-   Teach a team of other students how to effectively manufacture
    structures and electronics


<a id="org069cb31"></a>

## Design

-   Devise an inexpensive architecture, aiming to fit within a
    relatively low budget for such a project
-   Make the device look clean, modern, and monolithic from the
    audience's perspective
-   Primarily use available architectural materials, mostly wood, from
    the set workshop
-   Let the design be driven by requirements, and find the appropriate
    LED chips for the job
-   Come up with a switchable, cheap, easy to assemble current supply
    design using discrete components
-   Determine how to network many electronic parts together so that each
    receives necessary power
-   Use inexpensive computers to control the light array, writing all
    necessary algorithms by hand
-   Send images to the system remotely, from another computer, so that
    the operator may be elsewhere
-   Create cue software that enables graphical design of a sequential
    list of images for the display
-   Add an interface to the cue software to display images on the light
    array during the show


<a id="org06c6ddf"></a>

## Implementation

-   Manage and work with a team of people to assemble a massive object
    with many thousands of components
-   Find all necessary tools or parts and make sure that they are
    purchased when needed
-   Oversee inventory of components and equipment, looking out for
    losses or shortages
-   Instruct inexperienced students personally in disciplines like
    soldering and wiring
-   Work extensive quality control, fixing errors in construction that
    others failed to catch
-   Test all devices with care to ensure that nothing will break when
    the design scales up
-   Write hundreds of lines of code, fully test them, and optimize the
    software however needed
-   Lead the team, make sure there are tasks for people, and keep morale
    up throughout the project
-   Come up with fixes to unexpected issues right away, avoiding delays
    as much as possible
-   Do any critical job that abruptly comes up, spending as long as
    necessary to stay on track


<a id="org722d198"></a>

# System

![img](./LEDarchitecture.png)

// Convert to paragraphs

-   Origins
    -   I was given the original specification for this project near the
        end of the school year before the show
    -   The director wanted, essentially, a grid of independently
        controlled, colored lights
    -   This is, of course, significantly harder to actually do than it is
        to say
    -   He would agree that at the time, he had no idea of the complexity of
        what he was asking for
    -   At a design meeting the end of that year, I did some brainstorming
        and found a LED component that would work well
    -   I set to work over the summer coming up with a design that would
        achieve all of our goals

-   Driving considerations
    -   The first design aspect we were sure of was the size of one pixel:
        2 feet by 2 feet by 2 feet (for simplicity)
    -   This drove the size of the overall panel, which was chosen to be
        20 feet wide by 12 feet tall
    -   Shortly after, I decided on 3 watt red green blue LEDs, four per
        cube
    -   We knew that every pixel had to be independently and instantly
        controllable, in both color and brightness
    -   With these core points in mind, I had to design a system around
        them and to satisfy them

-   Structure
    -   Cubes
        -   All of our theatrical sets are constructed primarily from
            lumber, wood sheets, and screws
        -   These are the materials we had available, so these are the
            materials from which the Grid's body was built
        -   It was easy to envision each pixel of the display as an
            independent structural component: a cube
        -   Every cube was made of 12 lengths of 2x4 lumber, each about 2
            feet long, joined with construction screws
        -   The frames led to an unavoidable square border around each
            pixel, which turned out to look quite cool
        -   Channels were routed at appropriate locations in the frame to
            allow a sheet of plywood to be slid into place as a panel to
            mount electronics on
        -   Additional panels were applied to the sides of the cubes to
            prevent light from bleeding between them within the structure
        -   After LEDs were installed on the front of said panel, a sheet of
            translucent, diffusing plastic was stretched over the front of
            the cube to spread the light out and form a large square pixel
        -   As part of the process, areas of each cube were strategically
            painted black, which prevented the final Grid from looking, from
            the front, like it was made of wood
        -   Sixty cubes were manufactured in total; they were taken out to
            the stage and stacked in a rectangle, 10 by 6
        -   All cubes were carefully aligned to make the front surface would
            appear as flat and seamless as possible
        -   They were all screwed together in the back on all four sides,
            making the structure extremely solid
    
    -   Supports
        -   The Grid may have been large and sturdy, but it was narrow
            compared to its width, making it prone to tipping
        -   Since dozens of people were going to be working and acting
            around the structure for weeks, it was necessary to fix this
        -   Simply widening the base of the Grid would suffice, for which
            purpose supports needed to be added
        -   I added diagonal supports to the front first; these needed to be
            short to evade notice by the audience
        -   The front supports only extended by about a foot, but this was
            enough to prevent tipping in that direction, especially because
            everyone stayed well away to avoid damaging the plastic sheets
        -   Rear supports were much more important, as techs would be
            working behind the structure for long periods
        -   I connected four long supports to the back of the grid, running
            from the floor to the third cube up from the bottom
        -   Skids connecting the ends of the supports to the base of the
            Grid proper kept everything firmly attached
        -   These large supports made the Grid practically unshakable, and
            as safe as any of our other sets
        -   I and several others even took to climbing on the back of the
            structure to access difficult areas

-   Electronics
    -   Current Sources
        -   Knowing the kind of LED I would be using, I then needed to decide
            how to distribute power to all 240 of them
        -   An LED's brightness is a function of its current, and small
            variations in current can lead to significant fluctuations
        -   For this reason, I needed to ensure that constant current would
            pass thru each LED
        -   Every red green blue light emitting diode package in fact contains
            three independent LEDs, one of each color
        -   Every individual diode is rated for ~350 milliamps of current, so
            that is what I needed to provide
        -   I considered schemes to provide current to all three colors of a
            package with one circuit, but it would still have been possible
            for one chip to heat, draw more, and go into runaway
        -   In the end, it was necessary to include 720 independent current
            sources in the design, 0.35 A each
        -   It turned out to be far, far cheaper to purchase individual
            transistors and resistors with which to assemble current sources
            ourselves, as opposed to purchasing what was available
        -   Every cube (pixel) contained 12 current sources (4 LED
            packages \* 3 colors each); all were on the same circuit board
            and cooled with a PC case fan
        -   I designed the circuit and board layout in Kicad, did several
            prototyping passes, and taught others to build boards
        -   More discussion on this later, but our current sources, something
            like 15000 connections total, were all soldered by hand
    
    -   Power Supply
        -   Power into the auditorium stage is provided by 3 pin stage
            connectors, 120 volts at 60 hertz with a 20 amp maximum
        -   I needed to supply 720 independent current sources with 0.35
            amps direct current at around 3 volts
        -   The only way to do the step down safely was to use commodity
            power supplies
        -   The cheapest power supplies available supply 12 volts DC with a
            maximum of 30 amps of current
        -   These were the only commonly available supplies that satisfied
            my requirements without being too expensive; I acquired 10
        -   Each supply was to provide the power for one column of the Grid,
            or six circuit boards, or 72 current sources
        -   This is about 25 amps at 2.5 - 3.5 volts, but the supply voltage
            is mostly irrelevant because the current sources step it down
        -   That is not equivalent to 25 amps at 12 volts and so did not
            challenge the max power capability of the supplies; this
            prevented any voltage fluctuations or overheating
        -   A standard supply has a row of bare screw terminals, which are
            dangerous if uncovered, exposing people to line voltage
        -   These had to be dealt with, and we wanted switches and fuses on
            the power supplies, so covers were necessary
        -   I designed power supply covers in a CAD program, including holes
            for line power cable, output sockets, switch, fuses, voltmeter,
            and a cooling grille
        -   We had the covers and plastic feet to keep the supplies off wood
            3D printed, and assembled the final products
    
    -   Integration
        -   Having an electronic system design is one thing, but integrating
            it into a 12 foot high wooden structure is quite another
        -   As we finished building each cube, we affixed 4 LED packages to
            the mounting panel in its middle
        -   The LEDs went on the front of the panel, and all of the other
            electronics went on the back
        -   Before placing every LED, long connecting wires had to be
            soldered to its four pads and run through a hole to the back of
            the cube
        -   Thus, the Grid structure was built out of cubes onstage with all
            LEDs already installed
        -   After every circuit board was completed and tested, it had to be
            attached to the back of a cube's mounting panel
        -   Each circuit board had sixteen sockets for the sixteen wires
            from the LEDs, which had to be carefully connected with pliers
        -   In addition to those, there were three sockets for the control
            wires from the microcontrollers, which were much, much longer
            and had to be run across the back of the Grid and secured
        -   Sixty desktop computer case fans were acquired to cool the
            transistors of the circuit boards
        -   These, too, had to be mounted to the internal structure of the
            cube and connected to the circuit board for power
        -   The circuit boards could not be powered without the power
            supplies, which were placed in the third cube from the ground in
            each column
        -   Handmade power cables connected the supply output sockets to
            screw terminals on each circuit board
        -   More custom cables ran from the power supplies to backstage
            stage pin connectors

-   Software
    -   Microcontrollers
        -   Each cube had three colors of LED: red, green, and blue, which
            had to be controlled independently
        -   With 60 cubes and 3 colors per cube, 180 control channels were
            needed to switch all of the LEDs
        -   I needed cheap programmable boards with many 5 volt logic
            outputs, so I went with the Arduino Mega
        -   Since each Arduino has 54 logic outputs, we needed four of them
            to cover the 180 channels that controlled the Grid
        -   Each circuit board had three control inputs that were connected
            to Arduino logic outputs
        -   A HIGH signal turned on the LED, while a LOW signal kept it off
        -   LEDs, of course, have no brightness controls, so it is necessary
            to mediate the brightness by switching rapidly
        -   By turning them on and off many times per second, but changing
            the amount of time they are on during each second, the LEDs can
            be made to appear to change in brightness
        -   The ATmega processors used in the Arduino have a small number of
            hardware PWM outputs, but I needed every output to be capable of
            pulse width modulation
        -   I ended up having to implement PWM dimming in software, writing
            a program in C++ that switched the logic outputs many times
            every second and dimmed the LEDs
        -   This nearly did not work because the processors run at only 4
            MHz, but the Arduinos were just fast enough
        -   By dimming the different colors different amounts, any color
            that is a combination of light colors may be achieved
        -   It is necessary, during the show, to constantly communicate to
            the Arduinos whether any colors need to be changed
        -   They can receive data over a serial connection; luckily, the
            computer we used to oversee them had four USB ports
        -   Each Arduino kept a list containing the brightness of every one
            of its channels
        -   They were sent little "packets" over serial connection
            consisting of a header for alignment, a channel number, and a
            light intensity, each a single byte
        -   On every PWM cycle, the boards checked for new packets and
            changed the brightness of relevant channels accordingly
    
    -   Grid Server
        -   The four independent microcontrollers controlled the LEDs
            themselves, but they needed to be overseen
        -   For control of the entire Grid, a full fledged computer was
            necessary, so we got a Raspberry Pi 4
        -   This processor had a fast enough clock speed to communicate with
            an operator's client program and all four Arduinos at once
        -   It would be impractical for the Grid operator to be physically
            next to it at all times, so it was necessary to be able to send
            instructions about updating the display remotely
        -   This component is called the Grid server because it "serves"
            access to the Grid's physical display
        -   While the LEDs are connected to the Arduinos with hundreds of
            wires, the Arduinos connect to the server with only four USB
            cables
        -   The server itself, and by extension the entire Grid, is
            controlled over an Ethernet connection
        -   Our auditorium contains an isolated Ethernet network to control
            the many lighting fixtures, and it has ports in several
            convenient places, including backstage and the booth
        -   The server computer was connected to a backstage Ethernet port
            and assigned a static IP address
        -   The operator's computer, running the client program, was
            connected to an Ethernet port in the booth at the back of the
            auditorium, where the Grid is fully visible
        -   Listening on a TCP socket, the server made a connection with the
            client and prepared to receive control data
        -   Data came into the server in large chunks, with cube numbers
            associated with RGB color values
        -   The server mapped the cube numbers to the appropriate Arduinos
            and logic outputs thereof, and sent off serial packets
        -   Since packets were received over Ethernet and sent out over
            serial almost constantly, I placed these functions in separate
            threads so that they could run asynchronously
        -   This server computer was the point of access to the entire Grid,
            and I made an SSH connection into it and ran test and
            troubleshooting programs on many occasions
    
    -   Grid Client
        -   I give full credit for this impressive piece of software to one
            of my friends, a technician and actor who wrote it in just a
            couple weeks and saved the Grid
        -   It was important to have a piece of software from which the Grid
            could be easily controlled
        -   Just sending data remotely, however, is not nearly enough, as
            entering data to be displayed as RGB images by hand would take a
            prohibitively long time
        -   Thus, we needed a program that provided a graphical interface to
            the Grid: a list of cues to be replayed during shows, all
            created using a software representation of the Grid on which
            colors could be changed with a few clicks
        -   We needed both a graphical user interface and extremely fast
            development time, so we chose to use Python and the Qt framework
        -   Python is not a great language for application development, but
            it is quick to write and fast enough for this one time purpose
        -   The Qt framework provides a system to build graphical interfaces
            relatively easily, and bindings to the GUI components for use
            within an event driven program
        -   My friend built an interface that featured a scrollable cue list
            with editable cue names and numbers
        -   Next to the list was a representation of the Grid: 60 boxes,
            colored according to the design stored in the selected cue
        -   It was also possible to choose transitions between different
            cues and set their length
        -   The most used transition in our show was a smooth fade from one
            design to another
        -   An editing mode was included in the software, allowing the
            operator to select any cube and set its color, then send the
            result to the Grid for viewing
        -   There was also a blind mode, enabling editing of cues without
            changing what appeared on the Grid
        -   One fantastic feature was the ability to create animations and
            store them in a cue, which allowed effects like rain or a game
            of Tetris to be created
        -   All of the cues were stored in a custom text file format, which
            was written by the software on every change and read on startup
        -   The software used a small routine which I wrote to send packets
            full of color data to the Grid server
        -   The software was optimized with threading so that transitions
            could be run, and packets sent, without causing the GUI to hang
            and become unresponsive
        -   I was the Grid operator during all four shows, and the Grid
            client performed admirably throughout


<a id="orgebfdcf1"></a>

# Structure

![img](structure/grid_3.jpg)

// Finish


<a id="org42d862f"></a>

# Electronics

![img](electronics/current-sources/finished_boards_3.jpg)

// Finish


<a id="orgb3229b2"></a>

# Software

![img](software/control_interface_2.png)

// Finish


<a id="org93f03fa"></a>

# Reflection

![img](media/pictures/reflection.jpg)

// Finish

