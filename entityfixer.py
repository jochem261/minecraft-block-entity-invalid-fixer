import argparse
from os import path

from progress.bar import Bar

from nbt.nbt import TAG_Int
from nbt.region import RegionFile
from nbt.world import AnvilWorldFolder

WORLDS = {
    "Overworld": "",
    "Nether": "DIM-1/",
    "End": "DIM1/"
}

def to_int(value: TAG_Int) -> int:
    return int(value.value)

def in_chunk(chunk_x: int, chunk_z: int, x: TAG_Int, z: TAG_Int) -> bool:
    """
    Check if (x, z) is inside chunk.
    """
    chunk_x = chunk_x * 16
    chunk_z = chunk_z * 16

    x_int = to_int(x)
    z_int = to_int(z)

    return chunk_x <= x_int < chunk_x + 16 and chunk_z <= z_int < chunk_z + 16

def main(world_path: str, check: bool = False):
    total_found = 0

    for world in WORLDS.keys():
        print(f"Checking the {world}")
        world_folder = AnvilWorldFolder(path.join(world_path, WORLDS[world]))

        regions = world_folder.regionfiles

        if len(regions) == 0:
            print(f"Couldn't find region files for the {world}, skipping")
            continue

        with Bar("Checking Regions", fill="█", max=len(regions)) as bar:
            for region_coords in regions.keys():
                region = RegionFile(regions[region_coords])
                chunks = region.get_metadata()

                for chunk in chunks:
                    chunk_x = region_coords[0] * 32 + chunk.x
                    chunk_z = region_coords[1] * 32 + chunk.z

                    nbt = world_folder.get_nbt(chunk_x, chunk_z)
                    found_errors = False
                    entities = nbt["Level"]["TileEntities"]

                    for entity in entities:
                        if not in_chunk(chunk_x, chunk_z, entity['x'], entity['z']):
                            total_found += 1
                            found_errors = True

                            # Move the entity to the (hopefully) right coordinates
                            entity["x"].value = chunk_x  * 16 + (to_int(entity['x']) % 16)
                            entity["z"].value = chunk_z * 16 + (to_int(entity['z']) % 16)


                    if found_errors and not check:
                        region.write_chunk(chunk.x, chunk.z, nbt)

                bar.next()

        print(f"{ 'Found' if check else 'Fixed'} {total_found} entities with wrong coordinates")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("world_path", help="Path to your world file")
    parser.add_argument("--check", help="Only check for wrong entities, but don't fix them", action="store_true")
    args = parser.parse_args()

    main(world_path=args.world_path, check=args.check)