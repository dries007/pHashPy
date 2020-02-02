# Development Guide

_This is a copy of part of the [Development Guide](https://www.phash.org/docs/howto.html) from [pHash.org](https://www.phash.org/)._\
_Copyright (C) 2008-2010 Evan Klinger & David Starkweather_ \
_I made this archived copy to prevent it from being lost should the website go offline._

------------------------------------------------------------------------------

So far, pHash is capable of computing hashes for audio, video and image files. You start by computing hash values for the media files. The following are the function prototypes for the three methods:

    int ph_dct_imagehash(const char *file, ulong64 &hash);
    ulong64* ph_dct_videohash(const char *file, int &Length);
    uint32_t* ph_audiohash(float *buf, int N, int sr, int &nbFrames);

The image hash is returned in the hash parameter. Audio hashes are returned as an array of uint32_t types with the nbFrames parameter indicating the buffer length. Video hashes are returned as an array of uint64_t types with the Length parameter indicating the number of elements in the array. You must free the memory returned by ph_audiohash() and ph_dct_videohash() with free() when you are finished using it. For the audio hash, you must read the data into the buffer first. You do so with this function:

    float* ph_readaudio(const char *filename, int sr, int channels, int &N);

(It is recommended you use sr as 8000 and just one channel.) N will be the length of your returned buffer. You must free the memory returned by ph_readaudio() with free() when you are finished using it (usually after a call to ph_audiohash()).

There are image hash functions that use the radial hash projections method, rather than the discrete cosine transform (dct), but their results have not shown to be as good as the dct.

Once you have the hashes for two files, you can compare them. The functions you use to compare two files are as follows:

    int ph_hamming_distance(ulong64 hasha, ulong64 hashb);
    double* ph_audio_distance_ber(uint32_t *hasha, int Na, uint32_t *hashb, int Nb, float threshold, int block_size, int &Nc);

The hamming distance function can be used for both video and image hashes. For audio distance, the threshold should be around 0.30 (0.25 to 0.35), the block_size should be 256. The block_size is just the number of blocks of uint32 types to compare at a time in computing the bit error rate (ber) between two hashes. It returns a double buffer of length Nc, which is a confidence vector. It basically gives a confidence rating that indicates the similarity of two hashes at various positions of alignment. The maximum of this confidence vector should be a fairly good indication of similarity, a value of 0.5 being the threshold. You must free the memory returned by ph_audio_distance_ber() with free() when you are finished using it.

If you want to use the radial hashing method for images, the function for getting the hash is here:

    ph_image_digest(const char *file, double sigma, double gamma, Digest &dig, N);

Use values sigma=1.0 and gamma=1.0 for now. N indicates the number of lines to project through the center for 0 to 180 degrees orientation. Use 180. Be sure to declare a digest before calling the function, like this:

    Digest dig;
    ph_image_digest(filename, 1.0, 1.0, dig, 180);

The function returns -1 if it fails. This standard will be found in most of the functions in the pHash library.

To compare two radial hashes, a peak of cross correlation is determined between two hashes:

    int ph_crosscorr(Digest &x, Digest &y, double &pcc, double threshold=0.90);

The peak of cross correlation between the two vectors is returned in the pcc parameter.
