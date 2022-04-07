import json
import pygame
import pymunk
import os

class Tileset:
    def __init__(self, raw_dict, directory):
        self.columns = None                     # The number of columns in the sprite-sheet
        self.first_gid = None                   # The id number of the first tile (top-left).  Each tile after this
                                                #   is one larger, continuing with the rows below
        self.image = None                       # A pygame Surface
        self.margin = None                      # Not sure what this is -- perhaps a border around the tile data?
        self.spacing = None                     # The spacing (in pixels) between each tile
        self.tile_count = None                  # How many total tiles are there in this tileset?
        self.tile_height = None                 # The height (in pixels) of each tile in the image
        self.tile_width = None                  # The width (in pixels) of each tile in the image
        self.name = None                        # The name of the tileset (as it was labelled in tiled)

        if "columns" in raw_dict:           self.columns = raw_dict["columns"]
        if "firstgid" in raw_dict:          self.first_gid = raw_dict["firstgid"]
        if "image" in raw_dict:             self.image = pygame.image.load(directory + "/" + raw_dict["image"])
        if "margin" in raw_dict:            self.margin = raw_dict["margin"]
        if "name" in raw_dict:              self.name = raw_dict["name"]
        if "spacing" in raw_dict:           self.spacing = raw_dict["spacing"]
        if "tilecount" in raw_dict:         self.tile_count = raw_dict["tilecount"]
        if "tileheight" in raw_dict:        self.tile_height = raw_dict["tileheight"]
        if "tilewidth" in raw_dict:         self.tile_width = raw_dict["tilewidth"]

    def get_tile_data(self, code):
        if self.first_gid <= code <= self.first_gid + self.tile_count:
            tile_col = (code - self.first_gid) % self.columns
            tile_row = (code - self.first_gid) // self.columns
            return self.image, (tile_col * (self.tile_width + self.spacing),
                                tile_row * (self.tile_height + self.spacing),
                                self.tile_width, self.tile_height)
        return None

class Map:
    def __init__(self, fname):
        # Data about the map (will be filled in by parse_file, generally)
        self.fname = fname                      # The filename we're based on
        self.map_height = None                  # height of the map in tiles
        self.map_width = None                   # width of the map in tiles
        self.tile_width = None                  # width of each tile in pixels (of the map grid)
        self.tile_height = None                 # height of each tile in pixels (of the map grid)
        self.nextLayerID = None                 # The next layer id -- this value - 1 is the number of layers total
        self.nextObjectID = None                # The next object id -- this value - 1 is the number of objects total
        self.tile_sets = []
        self.tile_layers = []                   # stores all the tile layers in the map (in rows)
        self.pickups = []                       # a list of 2d points from the object layers of the map.  As the player
                                                #   collects these, the contents will change
        self.floor_points = []                  # Begin- and start positions of each platform.

        # Get some information about where the map file is located
        map_dir = os.path.dirname(fname)

        # Actually parse the map file (which should fill in most of the attributes "declared" above
        self.parse_file(fname, map_dir)

        # Create a few additional attributes / data from the newly processed map_data
        self.rendered_img = self.render_to_image()
        self.world_width = self.map_width * self.tile_width     # Width of the map, in pixels
        self.world_height = self.map_height * self.tile_height  # Height of the map, in pixels

    def parse_file(self, fname, directory):
        with open(fname, "r") as fp:
            raw_data = json.load(fp)

            # Pick out some top-level attribute values
            if "compressionlevel" in raw_data:          self.compression_level = raw_data["compressionlevel"]
            if "height" in raw_data:                    self.map_height = raw_data["height"]
            if "width" in raw_data:                     self.map_width = raw_data["width"]
            if "infinite" in raw_data:                  self.is_infinite = raw_data["infinite"]
            if "nextlayerid" in raw_data:               self.nextLayerID = raw_data["nextlayerid"]
            if "nextobjectid" in raw_data:              self.nextObjectID = raw_data["nextobjectid"]
            if "orientation" in raw_data:               self.orientation = raw_data["orientation"]
            if "renderorder" in raw_data:               self.render_order = raw_data["renderorder"]
            if "tiledversion" in raw_data:              self.map_version = raw_data["tiledversion"]
            if "tileheight" in raw_data:                self.tile_height = raw_data["tileheight"]
            if "tilewidth" in raw_data:                 self.tile_width = raw_data["tilewidth"]
            if "type" in raw_data:                      self.data_type = raw_data["type"]
            if "version" in raw_data:                   self.map_version = raw_data["version"]
            if "tiledversion" in raw_data:              self.tiled_version = raw_data["tiledversion"]


            if "layers" in raw_data:
                for layer in raw_data["layers"]:
                    self.process_layer(layer)

            if "tilesets" in raw_data:
                for ts in raw_data["tilesets"]:
                    self.tile_sets.append(Tileset(ts, directory))

    def process_layer(self, lyr):
        if "data" in lyr and len(lyr["data"]) == self.map_width * self.map_height:
            new_layer = []
            for i in range(self.map_height):
                start_index = i * self.map_width
                end_index = start_index + self.map_width
                row = lyr["data"][start_index:end_index]
                new_layer.append(row)
            self.tile_layers.append(new_layer)

        elif "objects" in lyr:
            for obj in lyr["objects"]:
                if "x" in obj and "y" in obj:
                    self.pickups.append((obj["x"], obj["y"]))

    def collider_on_platform(self, space, layer):
        y = 0

        for row in layer:
            x = 0
            last_placed_index = 0

            for tile_index in range(len(row)):  # for every tile in this row
                if tile_index <= last_placed_index and tile_index != 0:
                    continue

                tile_code = row[tile_index]
                if tile_code != 0:  # if there is a tile drawn on this row
                    start_x = tile_index * self.tile_width
                    end_x = start_x + self.tile_width

                    next_tile_index = tile_index + 1
                    while next_tile_index < len(row) and row[
                        next_tile_index] != 0:  # if there is ground on the next tile
                        end_x += self.tile_width
                        last_placed_index = next_tile_index
                        next_tile_index += 1

                    seg_up = pymunk.Segment(space.static_body, (start_x, y), (end_x, y), 0.0)
                    seg_up.elasticity = 0.95
                    seg_up.friction = 0.9
                    seg_bot = pymunk.Segment(space.static_body, (start_x, y + self.tile_height),
                                             (end_x, y + self.tile_height), 0.0)
                    seg_bot.elasticity = 0.95
                    seg_bot.friction = 0.9

                    self.floor_points.append([[start_x, end_x, y], [start_x, end_x, y + self.tile_height]])
                    space.add(seg_bot)
                    space.add(seg_up)

                x += self.tile_width
            y += self.tile_height

    def draw_colliders(self, space):
        self.collider_on_platform(space, self.tile_layers[0])
        self.collider_on_platform(space, self.tile_layers[1])

    def __str__(self):
        s = "Tilesets:\n"
        for i in range(len(self.tile_sets)):
            tset = self.tile_sets[i]
            s += "\tTileset" + str(i) + "(" + str(tset.name) + "):\n"
            s += "\t\tColumns: " + str(tset.columns) + "\n"
            s += "\t\tFirstGID: " + str(tset.first_gid) + "\n"
            s += "\t\tImage: " + str(tset.image) + "\n"
            s += "\t\tMargin: " + str(tset.margin) + " pixels\n"
            s += "\t\tSpacing: " + str(tset.spacing) + " pixels\n"
            s += "\t\tTileCount: " + str(tset.tile_count) + "\n"
            s += "\t\tTileDimensions: (" + str(tset.tile_width) + "x" + str(tset.tile_height) + ")\n"

        s += "TileLayers:\n"
        for i in range(len(self.tile_layers)):
            lyr = self.tile_layers[i]
            s += "\tLayer" + str(i) + ":\n"
            for row in lyr:
                s += "\t\t" + str(row) + "\n"
            if i < len(self.tile_layers) - 1:
                s += "\n"

        s += "Pickups: \n\t"
        for i in range(len(self.pickups)):
            s += str(self.pickups[i]) + "  "
            if i > 0 and i % 6 == 0:
                s += "\n"
                if i < len(self.pickups) - 1:
                    s += "\t"
        return s

    def get_tile_data(self, code):
        result = None
        for ts in self.tile_sets:
            ts_result = ts.get_tile_data(code)
            if ts_result is not None:
                result = ts_result
                break
        return result

    def render_to_image(self):
        surf = pygame.Surface((self.map_width * self.tile_width, self.map_height * self.tile_height))

        for layer in self.tile_layers:
            y = 0
            row_num = 0
            for row in layer:
                x = 0
                col_num = 0
                for code in row:
                    if code != 0:  # if there is a tile drawn on this row
                        result = self.get_tile_data(code)
                        if result is not None:
                            img, area = result
                            surf.blit(img, (x, y), area)
                    x += self.tile_width
                    col_num += 1
                y += self.tile_height
                row_num += 1

        return surf