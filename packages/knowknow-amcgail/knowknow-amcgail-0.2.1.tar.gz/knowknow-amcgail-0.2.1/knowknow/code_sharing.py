__all__ = [
    'kkmod'
]

modules = {
    'citation-deaths': "G:/My Drive/2020 ORGANISATION/1. PROJECTS/qualitative analysis of literature/110 CITATION ANALYSIS/010 analyses/bundle 101 - citation deaths reboot 10-2020",
    'wos-counter': "G:/My Drive/2020 ORGANISATION/1. PROJECTS/qualitative analysis of literature/110 CITATION ANALYSIS/010 analyses/bundle 102 - creating wos database",
    'stats': "G:/My Drive/2020 ORGANISATION/1. PROJECTS/qualitative analysis of literature/110 CITATION ANALYSIS/010 analyses/bundle 103 - various statistics"
    #'summary-stats': ""
}

mod_cache = {}

def kkmod( what ):
    wsp = what.split("/")
    space = wsp[0]

    from pathlib import Path
    if space not in modules:
        raise Exception('module space not found', space)
    
    spacefn = Path(modules[space])

    if len(wsp) == 2:
        # get it from __init__
        modfn = spacefn.joinpath("__init__.py")

    elif len(wsp) == 3:
        # get it from file within
        modfn = spacefn.joinpath("%s.py" % wsp[1])


    if modfn in mod_cache:
        mod = mod_cache[modfn]
    else:
        from runpy import run_path
        mod = run_path( modfn )

        if '__all__' in mod:
            mod = {
                k: v for k,v in mod.items() if k in mod['__all__']
            }

        mod_cache[modfn] = mod

    return mod[wsp[-1]]