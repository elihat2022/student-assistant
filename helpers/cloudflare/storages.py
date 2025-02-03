from storages.backends.s3 import S3Storage

class StaticFilesStorage(S3Storage):
    # helpers.cloudflare.storages.StaticFilesStorage
    location = 'static'
    
    
class MediaFilesStorage(S3Storage):
    # helpers.cloudflare.storages.MediaFilesStorage
    location = 'media'