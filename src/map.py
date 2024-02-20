import pygame
from pytmx import TiledImageLayer, TiledObjectGroup, TiledTileLayer
from pytmx.util_pygame import load_pygame

# based on https://github.com/bitcraft/pytmx/blob/master/apps/pygame_demo.py
class TiledMap(object):
    def __init__(self, filename) -> None:
        tm = load_pygame(filename)

        # self.size will be the pixel size of the map
        # this value is used later to render the entire map to a pygame surface
        self.pixel_size = tm.width * tm.tilewidth, tm.height * tm.tileheight
        self.tmx_data = tm

    def get_object_by_name(self, name):
        """Find a TiledObject with a name property"""
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, TiledObjectGroup):
                for obj in layer:
                    if obj.name == name:
                        return obj

    def get_first_tile_layer_index(self) -> int:
        """Get the first tile layer number"""
        for idx, layer in enumerate(self.tmx_data.visible_layers):
            if isinstance(layer, TiledTileLayer):
                return idx

    def get_tile_props_by_coords(self, layer_idx, x, y):
        """Find a TiledTile by pixel coordinates"""
        tile_gid = self.tmx_data.get_tile_gid(x, y, layer_idx)
        return self.tmx_data.get_tile_properties_by_gid(tile_gid)

    def render_map_to_new_surface(self) -> pygame.Surface:
        """Render our map to a new pygame surface

        This method returns a new surface with the map rendered onto it.
        The surface will be the same pixel size as the map.
        """

        # create a new surface with the correct pixel dimensions
        surface = pygame.Surface(self.pixel_size)

        # render the map onto the surface
        self.render_map(surface)

        return surface

    def render_map(self, surface) -> None:
        """Render our map to a pygame surface

        Feel free to use this as a starting point for your pygame app.
        This method expects that the surface passed is the same pixel
        size as the map.

        Scrolling is a often requested feature, but pytmx is a map
        loader, not a renderer!  If you'd like to have a scrolling map
        renderer, please see my pyscroll project.
        """

        # fill the background color of our render surface
        if self.tmx_data.background_color:
            surface.fill(pygame.Color(self.tmx_data.background_color))

        # iterate over all the visible layers, then draw them
        for layer in self.tmx_data.visible_layers:
            # each layer can be handled differently by checking their type

            if isinstance(layer, TiledTileLayer):
                self.render_tile_layer(surface, layer)
            # elif isinstance(layer, TiledObjectGroup):
            #     self.render_object_layer(surface, layer)
            # elif isinstance(layer, TiledImageLayer):
            #     self.render_image_layer(surface, layer)

    def render_tile_layer(self, surface, layer) -> None:
        """Render all TiledTiles in this layer"""
        # deref these heavily used references for speed
        tw = self.tmx_data.tilewidth
        th = self.tmx_data.tileheight
        surface_blit = surface.blit

        # iterate over the tiles in the layer, and blit them
        if self.tmx_data.orientation == "orthogonal":
            for x, y, image in layer.tiles():
                surface_blit(image, (x * tw, y * th))
        elif self.tmx_data.orientation == "isometric":
            ox = self.pixel_size[0] // 2
            tw2 = tw // 2
            th2 = th // 2
            for x, y, image in layer.tiles():
                sx = x * tw2 - y * tw2
                sy = x * th2 + y * th2
                surface_blit(image, (sx + ox, sy))

    def render_object_layer(self, surface, layer) -> None:
        """Render all TiledObjects contained in this layer"""
        # deref these heavily used references for speed
        draw_lines = pygame.draw.lines
        surface_blit = surface.blit

        # these colors are used to draw vector shapes,
        # like polygon and box shapes
        rect_color = (255, 0, 0)

        # iterate over all the objects in the layer
        # These may be Tiled shapes like circles or polygons, GID objects, or Tiled Objects
        for obj in layer:
            # logger.info(obj)

            # objects with points are polygons or lines
            if obj.image:
                # some objects have an image; Tiled calls them "GID Objects"
                surface_blit(obj.image, (obj.x, obj.y))

            else:
                # use `apply_transformations` to get the points after rotation
                draw_lines(surface, rect_color, obj.closed, obj.apply_transformations(), 3)

    def render_image_layer(self, surface, layer) -> None:
        if layer.image:
            surface.blit(layer.image, (0, 0))

    def list_all_tiles(self):
        all_tiles = []
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, TiledTileLayer):
                for x in range(self.tmx_data.width):
                    for y in range(self.tmx_data.height):
                        gid = layer.data[int(y)][int(x)]
                        if gid != 0:
                            tile_props = self.tmx_data.get_tile_properties_by_gid(gid)
                            all_tiles.append({
                                'x': x,
                                'y': y,
                                'gid': gid,
                                'props': tile_props
                            })
        return all_tiles
