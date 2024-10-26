using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class AvaterManager : MonoBehaviour
{
    AudioSource _audioSource;
    public AudioClip _audioClip;
    [SerializeField] private Animation[] _animation;
    [SerializeField] private GameObject _gameObject;

    void Start()
    {
        _audioSource = GetComponent<AudioSource>();
    }

    // ChatGPTから音声テキストを取得
    public void GetAudioText()
    {
        //_audioClip = () 代入
    }

    // 音声とアニメーションの再生
    public void PlayAnimation()
    {
        //if ()
        //{

        //}

        _audioSource.PlayOneShot(_audioClip);
    }
}
