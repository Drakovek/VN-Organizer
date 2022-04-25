#!/usr/bin/env python3

from math import atan, cos, degrees, sin
from PIL import Image, ImageDraw, ImageFont
from textwrap import wrap
from typing import List

def get_default_parameters() -> dict:
    params = {"node_width":150,
                "node_height":75,
                "node_buffer":3,
                "internode_buffer":20,
                "font_size":14,
                "outline_width":2,
                "font_color":"#ffffffff",
                "font_outline":"#000000ff",
                "outline_color":"#000000ff",
                "prompt_color":"#ff8000ff",
                "response_color":"#008000ff",
                "background_color":"#808080ff",
                "r":"#ff0000ff",
                "g":"#00ff00ff",
                "b":"#0000ffff",
                "c":"#00ffffff",
                "y":"#ffff00ff",
                "m":"#ff00ffff",
                "s":"#00ffffff",
                "d":"#ffffffff"}
    return params

def create_arrow(points:List=[],
                width:int=100,
                height:int=100,
                line_width:int=5,
                color:str="#000000ff") -> Image:
    # Create the canvas
    image = Image.new("RGBA", (width, height), "#ffffff00")
    # Create triangle
    draw = ImageDraw.Draw(image)
    radius = int(line_width * 2.5)
    # Get angle
    o = points["start"]["x"] - points["end"]["x"]
    a = points["start"]["y"] - points["end"]["y"]
    ang = atan(o/a)
    x = points["end"]["x"] - (sin(ang) * radius)
    y = points["end"]["y"] - (cos(ang) * radius)
    draw.regular_polygon(bounding_circle=(x, y, radius), n_sides=3,
                fill=color, rotation=degrees(ang)+180)
    # Draw line
    draw.line(xy=(points["start"]["x"], points["start"]["y"], x, y), fill=color, width=line_width)
    # Return the image
    return image

def create_rectangle(width:int=100,
                height:int=50,
                buffer:int=5,
                outline_width:int=2,
                fill_color:str="#ff0000ff",
                outline_color:str="#000000ff") -> Image:
    # Create points for the rectangle
    points = [(buffer, buffer),
                (buffer, buffer+height),
                (buffer+width, buffer+height),
                (buffer+width, buffer)]
    # Return the rectangle
    return create_polygon(points, width, height, buffer,
                outline_width, fill_color, outline_color)

def create_diamond(width:int=100,
                height:int=50,
                buffer:int=5,
                outline_width:int=2,
                fill_color:str="#ff0000ff",
                outline_color:str="#000000ff") -> Image:
    # Create points for the diamond
    midwidth = int((width+(buffer*2))/2)
    midheight = int((height+(buffer*2))/2)
    points = [(midwidth, buffer),
                (buffer, midheight),
                (midwidth, buffer+height),
                (buffer+width, midheight)]
    # Return the diamond
    return create_polygon(points, width, height, buffer,
                outline_width, fill_color, outline_color)

def create_hexagon(width:int=100,
                height:int=50,
                buffer:int=5,
                outline_width:int=2,
                fill_color:str="#ff0000ff",
                outline_color:str="#000000ff") -> Image:
    # Create points for the diamond
    int_width = int(width * 0.7)
    offset = int(((width + (buffer * 2)) - int_width)/2)
    back_offset = (width + (buffer*2)) - offset
    midheight = int((height+(buffer*2))/2)
    
    points = [(buffer, midheight),
                (offset, buffer),
                (back_offset, buffer),
                (width+buffer, midheight),
                (back_offset, height+buffer),
                (offset, height+buffer)]
    # Return the rectangle
    return create_polygon(points, width, height, buffer,
                outline_width, fill_color, outline_color)

def create_ellipse(width:int=100,
                height:int=100,
                buffer:int=5,
                outline_width:int=2,
                fill_color:str="#ff0000ff",
                outline_color:str="000000ff") -> List:
    # Create the canvas
    image = Image.new("RGBA", (width+(buffer*2), height+(buffer*2)), "#ffffff00")
    # Draw the polygon
    draw = ImageDraw.Draw(image)
    draw.ellipse([(buffer, buffer), (width+buffer, height+buffer)],
                fill=fill_color, outline=outline_color, width=outline_width)
    # Gets the connection points
    top_connect = {"x":int((width + (buffer * 2))/2), "y":buffer}
    bottom_connect = {"x":top_connect["x"], "y":(height+buffer)}
    # Return the image and connection points
    return {"top_connections":[top_connect],
                "bottom_connections":[bottom_connect],
                "image":image}

def create_polygon(points:List=[],
                width:int=100,
                height:int=100,
                buffer:int=5,
                outline_width:int=2,
                fill_color:str="#ff0000ff",
                outline_color:str="000000ff") -> dict:
    # Create the canvas
    image = Image.new("RGBA", (width+(buffer*2), height+(buffer*2)), "#ffffff00")
    # Draw the polygon
    draw = ImageDraw.Draw(image)
    draw.polygon(points, fill=fill_color, outline=outline_color, width=outline_width)
    # Gets the connection points
    top_connect = {"x":int((width + (buffer * 2))/2), "y":buffer}
    bottom_connect = {"x":top_connect["x"], "y":(height+buffer)}
    # Return the image and connection points
    return {"top_connections":[top_connect],
                "bottom_connections":[bottom_connect],
                "image":image}

def create_text(text:str=None,
            width:int=100,
            height:int=100,
            buffer:int=5,
            font_size:int=10,
            font_color:str="#ffffffff",
            font_outline:str="#000000ff") -> Image:
    # Create the canvas
    image = Image.new("RGBA", (width+(buffer*2), height+(buffer*2)), "#ffffff00")
    # Create the font
    try:
        # DejaVu
        font = ImageFont.truetype("DejaVuSans-Bold", size=font_size)
    except OSError:
        # Arial Black
        try:
            font = ImageFont.truetype(font="Arial_Black", size=font_size)
        except OSError:
            # Arial
            try:
                font = ImageFont.truetype(font="Arial", size=font_size)
            except OSError:
                # Default
                font = ImageFont.load_default()
    # Split text into lines
    lines = []
    char_width = (int(width / (font_size/2))) - 2
    for line in wrap(text, width=char_width):
        lines.append(str(line))
    # Draw lines of text
    stroke = int(font_size / 6)
    draw = ImageDraw.Draw(image)
    size = len(lines)
    space = int(font_size/4)
    block = (font_size * size) + (space * (size - 1))
    yoffset = int(((height + (buffer * 2)) - block) / 2)
    for i in range(0, size):
        w, h = draw.textsize(lines[i], font=font)
        xoffset = int(((width + (buffer*2)) - w)/2)
        y = (i * font_size) + yoffset
        y += (space * i)
        # Draw text line
        draw.text(text=lines[i], xy=(xoffset, y), font=font,
                    fill=font_color, align="center",
                    stroke_width=stroke, stroke_fill=font_outline)
    # Return the image
    return image

def add_offsets(points, offset):
    new_points = []
    for point in points:
        new_points.append({"x":(point["x"] + offset["x"]),
                    "y":(point["y"] + offset["y"])})
    return new_points

def overlap_images(back, front) -> Image:
    image = Image.new("RGBA", back.size, "#ffffff00")
    image.paste(back, (0,0))
    image.paste(front, (0,0), front)
    return image

def combine_horizontally(images:List, params:dict=get_default_parameters()) -> dict:
    # Return default if any of the given images are invalid
    mod_images = images
    while True:
        try:
            index = mod_images.index(None)
            del mod_images[index]
        except ValueError:
            break
    if len(mod_images) == 1:
        return mod_images[0]
    if len(mod_images) == 0:
        return None
    # Get the largest width and height of the image
    full_width = 0
    full_height = 0
    for im in images:
        w, h = im["image"].size
        full_width += w
        if h > full_height:
            full_height = h
    # Paste all the images together
    full_width += params["internode_buffer"] * (len(images) - 1)
    shapes = Image.new("RGBA", (full_width, full_height), "#ffffff00")
    x_offset = 0
    offsets = []
    for im in images:
        w, h = im["image"].size
        shapes.paste(im["image"], (x_offset, 0))
        offsets.append({"x":x_offset, "y":0})
        # Increment the x offset
        x_offset += w + params["internode_buffer"]
    # Get all the top and bottom connections
    top_connections = []
    bottom_connections = []
    for i in range(0, len(images)):
        top_connections.extend(add_offsets(images[i]["top_connections"], offsets[i]))
        bottom_connections.extend(add_offsets(images[i]["bottom_connections"], offsets[i]))
    # Return combined image
    return {"image":shapes,
                "top_connections":top_connections,
                "bottom_connections":bottom_connections}

def combine_vertically(images:List, params:dict=get_default_parameters()) -> Image:
    # Return default if any of the given images are invalid
    mod_images = images
    while True:
        try:
            index = mod_images.index(None)
            del mod_images[index]
        except ValueError:
            break
    if len(mod_images) == 1:
        return mod_images[0]
    if len(mod_images) == 0:
        return None
    # Get the largest width and height of the image
    full_width = 0
    full_height = 0
    for im in images:
        w, h = im["image"].size
        full_height += h
        if w > full_width:
            full_width = w
    # Paste all the images together
    full_height += params["internode_buffer"] * (len(images) - 1)
    shapes = Image.new("RGBA", (full_width, full_height), "#ffffff00")
    offsets = []
    y_offset = 0
    for im in images:
        w, h = im["image"].size
        x_offset = int((full_width - w) / 2)
        shapes.paste(im["image"], (x_offset, y_offset))
        offsets.append({"x":x_offset, "y":y_offset})
        # Increment the y offset
        y_offset += h + params["internode_buffer"]
    # Create arrow links
    arrows = Image.new("RGBA", (full_width, full_height), "#ffffff00")
    for i in range(1, len(images)):
        tops = add_offsets(images[i]["top_connections"], offsets[i])
        bottoms = add_offsets(images[i-1]["bottom_connections"], offsets[i-1])
        for j in range(0, len(images[i]["top_connections"])):
            # Create single arrow image
            arrow = create_arrow(points={"start": bottoms[j], "end": tops[j]},
                width=full_width,
                height=full_height,
                line_width=params["outline_width"],
                color=params["outline_color"])
            # Combine with the main arrow images
            arrows = overlap_images(arrows, arrow)
    # Combine shapes and arrows
    full_image = {"image":overlap_images(shapes, arrows),
                "top_connections":add_offsets(images[0]["top_connections"], offsets[0]),
                "bottom_connections":add_offsets(images[-1]["bottom_connections"], offsets[-1])}
    return full_image
    
def create_item_list_image(branch_dict:dict, params:dict=get_default_parameters()) -> Image:
    item_list = branch_dict["item_list"]
    image_list = []
    for item in item_list:
        # Get text image
        text = create_text(item["text"],
            width = params["node_width"],
            height = params["node_height"],
            buffer = params["node_buffer"],
            font_size = params["font_size"],
            font_color = params["font_color"],
            font_outline = params["font_outline"])
        # Get shape
        try:
            fill_color = params[item["type"].lower()]
        except KeyError:
            fill_color = params["d"]
        if item["type"] == "s":
            shape = create_ellipse(width = params["node_width"],
                    height = params["node_height"],
                    buffer = params["node_buffer"],
                    outline_width = params["outline_width"],
                    fill_color = fill_color,
                    outline_color = params["outline_color"])
        else:
            shape = create_hexagon(width = params["node_width"],
                    height = params["node_height"],
                    buffer = params["node_buffer"],
                    outline_width = params["outline_width"],
                    fill_color = fill_color,
                    outline_color = params["outline_color"])
        # Combine text and shape
        combined = {"image":overlap_images(shape["image"], text),
                    "top_connections":shape["top_connections"],
                    "bottom_connections":shape["bottom_connections"]}
        image_list.append(combined)
    # Combine list of images into one vertical stack
    full_image = combine_vertically(image_list)
    return full_image

def create_branch_header_image(branch_dict:dict, params:dict=get_default_parameters()) -> Image:
    # Create prompt node
    branches = branch_dict["branch"]
    text = create_text(branches[0]["prompt"],
                width = params["node_width"],
                height = params["node_height"],
                buffer = params["node_buffer"],
                font_size = params["font_size"],
                font_color = params["font_color"],
                font_outline = params["font_outline"])
    shape = create_diamond(width = params["node_width"],
                height = params["node_height"],
                buffer = params["node_buffer"],
                outline_width = params["outline_width"],
                fill_color = params["prompt_color"],
                outline_color = params["outline_color"])
    prompt = {"image": overlap_images(shape["image"], text)}
    bottom_connections = []
    for i in range(0, len(branches)):
        bottom_connections.append(shape["bottom_connections"][0])
    prompt["top_connections"] = shape["top_connections"]
    prompt["bottom_connections"] = bottom_connections
    # Create list of response nodes
    branch_imgs = []
    for branch in branches:
        text = create_text(branch["response"],
                width = params["node_width"],
                height = params["node_height"],
                buffer = params["node_buffer"],
                font_size = params["font_size"],
                font_color = params["font_color"],
                font_outline = params["font_outline"])
        shape = create_rectangle(width = params["node_width"],
                height = params["node_height"],
                buffer = params["node_buffer"],
                outline_width = params["outline_width"],
                fill_color = params["response_color"],
                outline_color = params["outline_color"])
        response = {"image": overlap_images(shape["image"], text),
                    "top_connections":shape["top_connections"],
                    "bottom_connections":shape["bottom_connections"]}
        branch_imgs.append(response)
    # Combine horizontally
    full_branch = combine_horizontally(branch_imgs)
    # Combine the prompt and response nodes
    full_image = combine_vertically([prompt, full_branch])
    return full_image
    
def generate_flowchart_node(branch_dict:dict, params:dict=get_default_parameters()) -> dict:
    # Get the item list
    item_list = None
    if len(branch_dict["item_list"]) > 0:
        item_list = create_item_list_image(branch_dict, params)
    # Get the branch header
    branch_image = None
    branches = branch_dict["branch"]
    if len(branches) > 0:
        branch_header = create_branch_header_image(branch_dict, params)
        # Get sub charts
        charts = []
        for branch in branches:
            charts.append(generate_flowchart_node(branch, params))
        # Combine sub charts
        branch_image = combine_vertically([branch_header, combine_horizontally(charts, params)], params)
    # Combine items and branch header
    top = combine_vertically([item_list, branch_image], params)
    # Return image
    return top

def generate_flowchart(branch_dict:dict, params:dict=get_default_parameters()) -> Image:
    # Get the full flowchart
    flowchart = generate_flowchart_node(branch_dict, params)
    if flowchart is None:
        background = Image.new("RGBA", (100, 100), params["background_color"])
        return background
    # Add background color
    w, h = flowchart["image"].size
    background = Image.new("RGBA", (w, h), params["background_color"])
    full = overlap_images(background, flowchart["image"])
    # Return the full image
    return full
